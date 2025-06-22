@app.route('/dashboard', methods=['GET'])
def get_dashboard_data():
    total_users = User.query.count()
    total_companies = Company.query.count()
    total_jobs = Job.query.count()
    total_applications = JobApplication.query.count()

    trends = []

    # Get the current time in Asia/Kolkata
    kolkata_tz = pytz.timezone('Asia/Kolkata')
    # Get the current time, localized to Kolkata
    now_kolkata = datetime.now(kolkata_tz)

    # Calculate data for the last 9 days
    for i in range(9):
        # Calculate the target date for 'i' days ago, maintaining Kolkata timezone awareness
        target_datetime_kolkata = now_kolkata - timedelta(days=i)

        # Extract the date part (year, month, day) from the Kolkata-aware datetime
        # We then construct naive datetimes for the start/end of THIS specific day in Kolkata time.
        # This assumes your DB stores naive datetimes that represent Kolkata time values.
        start_of_day_kolkata_naive = datetime(
            target_datetime_kolkata.year, target_datetime_kolkata.month, target_datetime_kolkata.day,
            0, 0, 0, 0 # Start of day, set microseconds to 0
        )
        end_of_day_kolkata_naive = datetime(
            target_datetime_kolkata.year, target_datetime_kolkata.month, target_datetime_kolkata.day,
            23, 59, 59, 999999 # End of day, set microseconds to 999999
        )

        # Count applications for the current day
        # Querying directly with naive datetimes that represent Kolkata time
        applications_count = JobApplication.query.filter(
            JobApplication.date_applied >= start_of_day_kolkata_naive,
            JobApplication.date_applied <= end_of_day_kolkata_naive
        ).count()

        # Count new logins (registrations) for the current day
        # Querying directly with naive datetimes that represent Kolkata time
        logins_count = Login.query.filter(
            Login.created_at >= start_of_day_kolkata_naive,
            Login.created_at <= end_of_day_kolkata_naive
        ).count()

        trends.append({
            # The 'x' value should still be the date in Kolkata time for consistent display on frontend.
            "x": target_datetime_kolkata.strftime("%Y-%m-%d"),
            "applications": applications_count,
            "logins": logins_count
        })

    # Reverse the list to have the most recent day last
    trends.reverse()

    return jsonify({
        "metrics": {
            "users": total_users,
            "companies": total_companies,
            "jobs": total_jobs,
            "applications": total_applications
        },
        "trends": trends
    })

