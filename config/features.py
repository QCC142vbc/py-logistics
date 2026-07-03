from pydantic import BaseSettings


class FeatureFlags(BaseSettings):
    """Feature flags configuration."""

    enable_simulation: bool = True
    enable_advanced_analytics: bool = True
    enable_ml_forecasting: bool = False
    enable_real_time_tracking: bool = True

    class Config:
        env_prefix = "FEATURE_"
