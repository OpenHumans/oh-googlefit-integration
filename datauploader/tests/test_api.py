from datauploader import googlefit_api as API


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

    dataset1 = {'steps': {'from_gps': {'2017-10-01': ['data1'], '2017-10-09': ['data2']}}}

    dataset2 = {'steps': {'from_gps': {'2017-10-09': ['data2','data3'],
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
