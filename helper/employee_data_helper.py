from helper import calculate_time_difference_in_hours

rest_time = 1.5


async def process_employee_data(data):
    if data is None:
        return []

    process_data = []
    for item in data:
        each_item = dict(item)
        each_item['rest'] = rest_time

        if each_item['clockin'] is not None and each_item['clockout'] is not None:
            total_work_time = calculate_time_difference_in_hours(
                each_item['clockin'],
                each_item['clockout']
            )
            each_item['total_work_ime'] = total_work_time
        else:
            each_item['total_work_ime'] = 0
        process_data.append(each_item)
    return process_data
