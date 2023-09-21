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


async def check_clockin_or_clockout(data, clockin, clockout):
    results = []

    for item in data:
        each_item = dict(item)
        id = each_item['id']

        if not each_item['clockin']:
            if clockin is not None and clockout is None:
                res = clockin < each_item['clockout']
                results.append((id, res))

        if not each_item['clockout']:
            if clockin is None and clockout is not None:
                res = clockout > each_item['clockin']
                results.append((id, res))

    return results


async def process_employee_exist_data(data):
    process_data = dict(data)
    box = []

    for item in process_data:
        box.append(item)
        box.append(process_data[item])
        break

    return box
