#!/usr/bin/env python3
"""
Test script to verify the tennis booking assistant setup.
"""

import sys
from pathlib import Path
from datetime import date

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))


def test_imports():
    """Test that all modules can be imported."""
    print("🔍 Testing imports...")

    try:
        from data.courts import COURT_ATTRIBUTES, get_court_by_id

        print("✅ Courts module imported successfully")

        from data.user_preferences import user_preferences

        print("✅ User preferences module imported successfully")

        from booking.stc_client import stc_client

        print("✅ STC client module imported successfully")

        from agent.tennis_agent import TennisBookingAgent

        print("✅ Tennis agent module imported successfully")

        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False


def test_court_data():
    """Test court data functionality."""
    print("\n🎾 Testing court data...")

    from data.courts import (
        COURT_ATTRIBUTES,
        get_court_by_id,
        get_courts_by_type,
        get_wingfield_courts,
    )

    print(f"✅ Found {len(COURT_ATTRIBUTES)} courts")

    # Test court lookup
    court = get_court_by_id("court_1")
    if court:
        print(f"✅ Court lookup works: {court.name}")

    # Test court type filtering
    sand_courts = get_courts_by_type("sand")
    print(f"✅ Found {len(sand_courts)} sand courts")

    # Test Wingfield courts
    wingfield_courts = get_wingfield_courts()
    print(f"✅ Found {len(wingfield_courts)} Wingfield courts")
    if wingfield_courts:
        print(f"   - Wingfield court: {wingfield_courts[0].name}")

    return True


def test_user_preferences():
    """Test user preferences functionality."""
    print("\n👤 Testing user preferences...")

    from data.user_preferences import user_preferences

    # Test getting preferences
    laura_prefs = user_preferences.get_preferred_courts("Laura")
    print(f"✅ Laura's preferred courts: {laura_prefs}")

    laura_types = user_preferences.get_preferred_court_types("Laura")
    print(f"✅ Laura's preferred court types: {laura_types}")

    # Test exclusion functionality
    laura_excluded = user_preferences.get_excluded_courts("Laura")
    print(f"✅ Laura's excluded courts: {laura_excluded}")

    # Test court exclusion check
    is_court_1_excluded = user_preferences.is_court_excluded("Laura", "court_1")
    is_court_15_excluded = user_preferences.is_court_excluded("Laura", "court_15")
    print(f"✅ Laura excludes court_1: {is_court_1_excluded}")
    print(f"✅ Laura excludes court_15: {is_court_15_excluded}")

    return True


def test_stc_client():
    """Test STC client functionality."""
    print("\n🌐 Testing STC client...")

    from booking.stc_client import stc_client

    try:
        # Test fetching availability for today
        today = date.today()
        availability = stc_client.get_court_availability(today)

        if availability:
            print(f"✅ Successfully fetched availability for {len(availability)} courts")
            for court_avail in availability[:3]:  # Show first 3
                print(
                    f"   - {court_avail.court_name}: {len(court_avail.time_slots)} slots"
                )
        else:
            print("⚠️ No availability data returned (this might be normal)")

        return True
    except Exception as e:
        print(f"❌ STC client error: {e}")
        return False


def test_agent():
    """Test tennis agent functionality."""
    print("\n🤖 Testing tennis agent...")

    from agent.tennis_agent import TennisBookingAgent

    try:
        # Create agent with dummy API key for testing
        agent = TennisBookingAgent("dummy-key")
        print("✅ Tennis agent created successfully")

        # Test request parsing
        test_message = "I want to play tennis tomorrow at 3pm"
        request = agent._parse_user_request(test_message)

        if request.target_date:
            print(f"✅ Request parsing works: {request.target_date}")

        return True
    except Exception as e:
        print(f"❌ Agent error: {e}")
        return False


def main():
    """Run all tests."""
    print("🧪 Testing Tennis Booking Assistant Setup\n")

    tests = [
        test_imports,
        test_court_data,
        test_user_preferences,
        test_stc_client,
        test_agent,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")

    print(f"\n📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! The setup is working correctly.")
        print("\nTo run the application:")
        print("1. Create a .env file with your OPENAI_API_KEY")
        print("2. Run: python run.py")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
