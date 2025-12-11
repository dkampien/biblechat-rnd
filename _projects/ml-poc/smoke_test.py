"""
Kumo SDK Smoke Test
===================
Validates that KumoRFM + LocalGraph works with local pandas DataFrames.

Run: python smoke_test.py
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Step 0.1: Test basic imports
print("=" * 50)
print("Step 0.1: Testing imports...")
print("=" * 50)

try:
    import kumoai
    print(f"✓ kumoai imported (version: {getattr(kumoai, '__version__', 'unknown')})")
except ImportError as e:
    print(f"✗ Failed to import kumoai: {e}")
    print("  Run: pip install kumoai")
    exit(1)

try:
    import pandas as pd
    print(f"✓ pandas imported (version: {pd.__version__})")
except ImportError as e:
    print(f"✗ Failed to import pandas: {e}")
    exit(1)

try:
    from kumoai.experimental.rfm import LocalGraph, KumoRFM
    print("✓ LocalGraph and KumoRFM imported from kumoai.experimental.rfm")
except ImportError as e:
    print(f"✗ Failed to import LocalGraph/KumoRFM: {e}")
    print("  This may indicate the RFM path is not available in your kumoai version.")
    print("  Fallback: Try the full SDK with upload_table() + FileUploadConnector")
    exit(1)

print("\n")

# Step 0.2: Test tiny DataFrame creation + LocalGraph
print("=" * 50)
print("Step 0.2: Testing LocalGraph with tiny DataFrame...")
print("=" * 50)

users_df = pd.DataFrame({
    'user_id': ['u1', 'u2', 'u3', 'u4', 'u5'],
    'created_at': pd.date_range('2024-01-01', periods=5)
})

events_df = pd.DataFrame({
    'event_id': [f'e{i}' for i in range(20)],
    'user_id': ['u1', 'u1', 'u1', 'u2', 'u2', 'u2', 'u3', 'u3', 'u3', 'u3',
                'u4', 'u4', 'u4', 'u4', 'u4', 'u5', 'u5', 'u5', 'u5', 'u5'],
    'ts': pd.date_range('2024-01-01', periods=20, freq='D'),
    'event_type': ['habitDone'] * 10 + ['ahaBedtimeStories'] * 10
})

print(f"Users DataFrame: {len(users_df)} rows")
print(users_df.to_string(index=False))
print(f"\nEvents DataFrame: {len(events_df)} rows")
print(events_df.head(10).to_string(index=False))
print("...")

try:
    graph = LocalGraph.from_data({
        'users': users_df,
        'events': events_df
    })
    print(f"\n✓ LocalGraph created successfully")
    print(f"  Graph object: {graph}")
except Exception as e:
    print(f"\n✗ Failed to create LocalGraph: {e}")
    exit(1)

print("\n")

# Step 0.3: Test basic PQL query
print("=" * 50)
print("Step 0.3: Testing basic PQL query...")
print("=" * 50)

# Check if API key is set and initialize client
api_key = os.getenv('KUMO_API_KEY')
api_url = os.getenv('KUMO_API_URL', 'https://kumorfm.ai/api')  # KumoRFM SaaS endpoint

if api_key:
    print(f"✓ KUMO_API_KEY found (length: {len(api_key)} chars)")
    print(f"✓ KUMO_API_URL: {api_url}")
    # Initialize the Kumo client with API key AND URL
    kumoai.init(url=api_url, api_key=api_key)
    print("✓ kumoai.init() called with API key and URL")
else:
    print("✗ KUMO_API_KEY not set - cannot proceed with prediction")
    exit(1)

try:
    rfm = KumoRFM(graph)
    print(f"✓ KumoRFM instance created")

    # Simple query: predict if user will have any events in next 7 days (shorter window for tiny dataset)
    query = "PREDICT COUNT(events.*, 0, 7, days) > 0 FOR EACH users.user_id"
    print(f"\nRunning query: {query}")

    # Pass the user IDs we want predictions for
    user_ids = users_df['user_id'].tolist()
    print(f"Predicting for users: {user_ids}")

    result = rfm.predict(query, indices=user_ids)
    print(f"\n✓ Query executed successfully!")
    print(f"Result type: {type(result)}")
    print(f"Result:\n{result}")

except Exception as e:
    print(f"\n✗ Query failed: {e}")
    print(f"  Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()

print("\n")
print("=" * 50)
print("SMOKE TEST COMPLETE")
print("=" * 50)
print("""
Next steps:
- If all steps passed: Proceed with Phase 1 (Data Generation)
- If Step 0.2 failed: Check kumoai version, try full SDK path
- If Step 0.3 failed: Check API key, check PQL syntax, review error message
""")
