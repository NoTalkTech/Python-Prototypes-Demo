import numpy as np
import pandas as pd
import logging
import sys
from typing import Union, List, Optional
from colorlog import ColoredFormatter

formatter = ColoredFormatter(
    '%(log_color)s[%(asctime)s]{%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white'
    }
)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)

logging.basicConfig(level=logging.INFO, handlers=[handler])

def calculate_iv(data: pd.DataFrame,
                feature: str,
                target: str,
                bins: Optional[Union[int, List[float]]] = 10,
                labels: Optional[List[str]] = None,
                binning_method: str = 'quantile') -> float:
    """Calculate Information Value (IV) for a feature.
    
    Args:
        data: DataFrame containing the feature and target
        feature: Name of the feature column
        target: Name of the target column (binary: 0/1)
        bins: Number of bins for continuous features or list of bin edges
        labels: Optional list of labels for the bins
        binning_method: Method for binning continuous features ('quantile', 'equal_width', 'tree')
    
    Returns:
        float: Information Value of the feature
    """
    df = data[[feature, target]].copy()
    
    # Handle missing values
    if df[feature].isnull().any():
        logging.warning(f"Feature {feature} contains {df[feature].isnull().sum()} missing values")
        df = df.fillna({feature: 'MISSING'})
    
    # Bin continuous features
    if pd.api.types.is_numeric_dtype(df[feature]):
        if isinstance(bins, int):
            if binning_method == 'quantile':
                df['bin'] = pd.qcut(df[feature], q=bins, labels=labels, duplicates='drop')
            elif binning_method == 'equal_width':
                df['bin'] = pd.cut(df[feature], bins=bins, labels=labels)
            elif binning_method == 'tree':
                from sklearn.tree import DecisionTreeClassifier
                # Use decision tree to find optimal bin boundaries
                tree = DecisionTreeClassifier(max_leaf_nodes=bins, random_state=42)
                tree.fit(df[feature].values.reshape(-1, 1), df[target])
                # Get decision boundaries from tree
                thresholds = sorted(list(set(tree.tree_.threshold[tree.tree_.threshold != -2])))
                bin_edges = [-np.inf] + thresholds + [np.inf]
                df['bin'] = pd.cut(df[feature], bins=bin_edges, labels=labels)
            else:
                raise ValueError(f"Unknown binning method: {binning_method}")
        else:
            df['bin'] = pd.cut(df[feature], bins=bins, labels=labels)
    else:
        df['bin'] = df[feature]
    
    # Calculate WOE and IV
    grouped = df.groupby('bin', observed=True)[target].agg(['count', 'sum'])
    grouped.columns = ['total', 'bad']
    grouped['good'] = grouped['total'] - grouped['bad']
    
    total_good = grouped['good'].sum()
    total_bad = grouped['bad'].sum()
    
    grouped['bad_rate'] = grouped['bad'] / total_bad
    grouped['good_rate'] = grouped['good'] / total_good
    
    # Handle zero counts
    eps = 1e-10
    grouped['woe'] = np.log((grouped['bad_rate'] + eps) / (grouped['good_rate'] + eps))
    grouped['iv'] = (grouped['bad_rate'] - grouped['good_rate']) * grouped['woe']
    
    iv_value = grouped['iv'].sum()
    
    # Log detailed information
    logging.info(f"\nIV calculation for feature: {feature}" + 
                 "\n++++++++++++++++++++ [Detailed statistics] ++++++++++++++++++++\n" + 
                 grouped.head(10).to_string() + 
                 "\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n" + 
                 f"\nTotal IV: {iv_value:.4f}")
    
    # Interpretation guide
    if iv_value < 0.02:
        logging.info("Predictive Power: Not useful for prediction")
    elif iv_value < 0.1:
        logging.info("Predictive Power: Weak")
    elif iv_value < 0.3:
        logging.info("Predictive Power: Medium")
    else:
        logging.info("Predictive Power: Strong")
        
    return iv_value

def calculate_iv_batch(data: pd.DataFrame,
                      features: List[str],
                      target: str,
                      bins: int = 10) -> pd.DataFrame:
    """Calculate IV for multiple features.
    
    Args:
        data: DataFrame containing features and target
        features: List of feature names
        target: Name of the target column
        bins: Number of bins for continuous features
        
    Returns:
        DataFrame: IV values for all features, sorted by IV
    """
    iv_values = []
    for feature in features:
        try:
            iv = calculate_iv(data, feature, target, bins)
            iv_values.append({'Feature': feature, 'IV': iv})
        except Exception as e:
            logging.error(f"Error calculating IV for {feature}: {str(e)}")
            continue
    
    iv_df = pd.DataFrame(iv_values)
    iv_df = iv_df.sort_values('IV', ascending=False)
    
    logging.info("\nIV Summary for all features:\n" + iv_df.to_string())
    
    return iv_df

# Mock test data and test functions
if __name__ == "__main__":
    # Create mock data
    np.random.seed(42)
    n_samples = 1000
    
    # Test case 1: Numeric features with strong predictive power
    mock_data = pd.DataFrame({
        'income': np.random.normal(50000, 20000, n_samples),
        'age': np.random.randint(18, 80, n_samples),
        'credit_score': np.random.randint(300, 850, n_samples),
        'target': np.random.binomial(1, 0.3, n_samples)
    })
    
    # Add some missing values
    mock_data.loc[np.random.choice(n_samples, 50), 'income'] = np.nan
    
    # Test case 2: Categorical feature
    mock_data['education'] = np.random.choice(
        ['High School', 'Bachelor', 'Master', 'PhD'],
        n_samples
    )
    
    # Test individual feature
    logging.info("============ Testing calculate_iv with numeric feature: =============")
    iv_income = calculate_iv(mock_data, 'income', 'target', bins=5,  binning_method = 'tree')
    logging.info(f"IV for income feature => {iv_income}")
    
    logging.info("============ Testing calculate_iv with categorical feature: =============")
    iv_education = calculate_iv(mock_data, 'education', 'target')
    logging.info(f"IV for education feature => {iv_education}")
    
    # Test batch calculation
    logging.info("============ Testing calculate_iv_batch: =============")
    features = ['age', 'credit_score', 'education']
    iv_results = calculate_iv_batch(mock_data, features, 'target', bins=5)
    logging.info(iv_results)

    # Test edge cases
    logging.info("============ Testing edge cases: =============")
    
    # Case 1: All same values
    mock_data['constant'] = 1
    try:
        iv_constant = calculate_iv(mock_data, 'constant', 'target')
    except Exception as e:
        logging.info(f"Expected error for constant feature => {str(e)}")
    
    # Case 2: All missing values
    mock_data['all_missing'] = np.nan
    iv_missing = calculate_iv(mock_data, 'all_missing', 'target')
    logging.info(f"IV for all missing feature => {iv_missing}")
    
    # Case 3: Binary feature
    mock_data['binary'] = np.random.binomial(1, 0.5, n_samples)
    iv_binary = calculate_iv(mock_data, 'binary', 'target')
    logging.info(f"IV for binary feature => {iv_binary}")
