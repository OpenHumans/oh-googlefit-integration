from datetime import datetime
from datauploader import googlefit_api as API

from doubles import expect, allow


def test_daterange_across_months_should_create_two_files():
    start_sync_dt = datetime(2018, 3, 26, 12, 5, 1)
    curr_dt = datetime(2018, 4, 1, 0, 0, 1)
    number_of_days = 7
    data_type = 'com.google.step_count.delta'
    data_source = 'derived:com.google.step_count.delta:com.google.android.gms:merge_step_deltas'

    expect(API).get_last_synced_data.and_return((None, start_sync_dt))
    expect(API).query_data_sources.and_return({(data_type, data_source)})
    expect(API).query_data_stream.and_return({}).exactly(number_of_days).times
    res = API.get_googlefit_data('', '', curr_dt)
    assert len(res) == 2
    assert res[0][1] == '2018-03'
    assert res[1][1] == '2018-04'


def monthly_ranges_should_work_for_long_range_spanning_many_months():
    start_dt = datetime(2017, 9, 2, 4, 4, 2)
    end_dt = datetime(2018, 1, 5, 4, 4, 6)
    ranges = list(API.generate_monthly_ranges(start_dt, end_dt))
    expected = [(start_dt, API.end_of_day(datetime(2017, 9, 30))),
                (API.start_of_day(datetime(2017, 10, 1)), API.end_of_day(datetime(2017, 10, 31))),
                (API.start_of_day(datetime(2017, 11, 1)), API.end_of_day(datetime(2017, 11, 30))),
                (API.start_of_day(datetime(2017, 12, 1)), API.end_of_day(datetime(2017, 12, 31))),
                (API.start_of_day(datetime(2018, 1, 1)), end_dt)
                ]

    assert (ranges == expected)


def monthly_ranges_should_work_for_short_range_within_same_month():
    start_dt = datetime(2017, 9, 2, 4, 4, 2)
    end_dt = datetime(2017, 9, 5, 4, 4, 6)
    ranges = list(API.generate_monthly_ranges(start_dt, end_dt))
    expected = [(start_dt, end_dt)]
    assert (ranges == expected)


def monthly_ranges_should_work_for_same_date():
    start_dt = datetime(2017, 9, 2, 4, 4, 2)
    end_dt = datetime(2017, 9, 2, 23, 4, 2)
    ranges = list(API.generate_monthly_ranges(start_dt, end_dt))
    expected = [(start_dt, end_dt)]
    assert (ranges == expected)


def monthly_ranges_should_work_for_leap_years():
    start_dt = datetime(2016, 1, 2, 4, 4, 2)
    end_dt = datetime(2016, 3, 5, 4, 4, 6)
    ranges = list(API.generate_monthly_ranges(start_dt, end_dt))
    expected = [(start_dt, API.end_of_day(datetime(2016, 1, 31))),
                (API.start_of_day(datetime(2016, 2, 1)), API.end_of_day(datetime(2016, 2, 29))),
                (API.start_of_day(datetime(2016, 3, 1)), end_dt)
                ]

    assert (ranges == expected)


def merging_datasets_without_daily_overlap_should_work():
    pairs = [('steps', 'from_gps')]
    data_types = ['steps']

    dataset1 = {'steps': {'from_gps': {'2017-10-01': ['data1'], '2017-10-09': ['data2']}}}

    dataset2 = {'steps': {'from_gps': {'2017-10-10': ['data3'],
                                       '2017-10-11': ['data4']}}}

    dataset_merged = {'steps': {'from_gps': {'2017-10-01': ['data1'], '2017-10-09': ['data2'], '2017-10-10': ['data3'],
                                             '2017-10-11': ['data4']}}}

    gf1 = API.GoogleFitData(dataset1,
                            {'month': '10-2017', 'last_dt': '2017-10-09 12:30:41', 'data_source_pairs': pairs,
                             'data_types': data_types})
    gf2 = API.GoogleFitData(dataset2,
                            {'month': '10-2017', 'last_dt': '2017-10-12 12:30:41', 'data_source_pairs': pairs,
                             'data_types': data_types})

    expected = API.GoogleFitData(dataset_merged,
                                 {'month': '10-2017', 'last_dt': '2017-10-12 12:30:41', 'data_source_pairs': pairs,
                                  'data_types': data_types})

    assert (gf1.merge(gf2) == expected)
    assert (gf2.merge(gf1) == expected)


def merging_datasets_with_daily_overlap_should_work():
    pairs = [('steps', 'from_gps')]
    data_types = ['steps']

    dataset1 = {'steps': {'from_gps': {'2017-10-01': ['data1'], '2017-10-09': ['data2', []]}}}

    dataset2 = {'steps': {'from_gps': {'2017-10-09': ['data2', 'data3'],
                                       '2017-10-11': ['data4']}}}

    # for the day present in both datasets -> we should get the longest dataset, ie '2017-10-09': ['data2', 'data3']
    dataset_merged = {'steps': {'from_gps': {'2017-10-01': ['data1'], '2017-10-09': ['data2', 'data3'],
                                             '2017-10-11': ['data4']}}}

    gf1 = API.GoogleFitData(dataset1,
                            {'month': '10-2017', 'last_dt': '2017-10-09 12:30:41', 'data_source_pairs': pairs,
                             'data_types': data_types})
    gf2 = API.GoogleFitData(dataset2,
                            {'month': '10-2017', 'last_dt': '2017-10-12 12:30:41', 'data_source_pairs': pairs,
                             'data_types': data_types})

    expected = API.GoogleFitData(dataset_merged,
                                 {'month': '10-2017', 'last_dt': '2017-10-12 12:30:41', 'data_source_pairs': pairs,
                                  'data_types': data_types})

    assert (gf1.merge(gf2) == expected)
    assert (gf2.merge(gf1) == expected)
