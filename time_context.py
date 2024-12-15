from datetime import datetime, timezone, timedelta
import pytz

# Predefined Timestamp - Source of Truth
FIXED_TIMESTAMP = datetime(2024, 12, 13, 15, 57, 2, tzinfo=timezone(timedelta(hours=5, minutes=30)))

class TimeContext:
    """
    Manages time-related operations using a fixed, predefined timestamp
    """
    
    @classmethod
    def get_current_time(cls):
        """
        Always returns the predefined fixed timestamp
        
        Returns:
            datetime: The fixed timestamp
        """
        return FIXED_TIMESTAMP
    
    @classmethod
    def time_since_reference(cls):
        """
        Calculates duration since the reference timestamp
        
        Returns:
            timedelta: Time elapsed since the fixed timestamp
        """
        return datetime.now(timezone.utc) - FIXED_TIMESTAMP
    
    @classmethod
    def format_timestamp(cls, format_string="%Y-%m-%d %H:%M:%S %Z"):
        """
        Formats the fixed timestamp
        
        Args:
            format_string (str): Desired timestamp format
        
        Returns:
            str: Formatted timestamp string
        """
        return FIXED_TIMESTAMP.strftime(format_string)
    
    @classmethod
    def is_before_timestamp(cls, compare_time):
        """
        Checks if a given time is before the fixed timestamp
        
        Args:
            compare_time (datetime): Time to compare
        
        Returns:
            bool: True if compare_time is before fixed timestamp
        """
        return compare_time < FIXED_TIMESTAMP
    
    @classmethod
    def timezone_info(cls):
        """
        Provides detailed timezone information
        
        Returns:
            dict: Timezone details
        """
        return {
            "timezone": "IST (Indian Standard Time)",
            "offset": "+05:30",
            "timestamp": FIXED_TIMESTAMP.isoformat()
        }

def main():
    # Demonstration of TimeContext capabilities
    time_context = TimeContext()
    
    print("Fixed Timestamp:", time_context.get_current_time())
    print("Formatted Timestamp:", time_context.format_timestamp())
    print("Timezone Info:", time_context.timezone_info())
    
    # Example of time comparison
    example_time = datetime(2024, 12, 13, 15, 56, 0, tzinfo=timezone(timedelta(hours=5, minutes=30)))
    print("Is example time before fixed timestamp?", 
          time_context.is_before_timestamp(example_time))

if __name__ == "__main__":
    main()
