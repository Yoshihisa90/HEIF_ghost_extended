# Common constants

FILE_NAME = [
   '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
   '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
   '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
   '31', '32', '33', '34', '35', '36', '37', '38', '39', '40',
   '41', '42', '43', '44', '45', '46', '47', '48', '49', '50',
   '51', '52', '53', '54', '55', '56', '57', '58', '59', '60',
   '61', '62', '63', '64', '65', '66', '67', '68', '69', '70',
   '71', '72', '73', '74', '75', '76', '77', '78', '79', '80',
   '81', '82', '83', '84', '85', '86', '87', '88', '89', '90',
   '91', '92', '93', '94', '95', '96', '97', '98', '99', '100',
   '101', '102', '103', '104', '105', '106', '107', '108', '109', '110',
   '111', '112', '113', '114', '115', '116', '117', '118', '119', '120',
   '121', '122', '123', '124', '125', '126', '127', '128', '129', '130',
   '131', '132', '133', '134', '135', '136', '137', '138', '139', '140',
   '141', '142', '143', '144', '145', '146', '147', '148', '149', '150',
    '151', '152', '153', '154', '155', '156', '157', '158', '159', '160', 
    '161', '162', '163', '164', '165', '166', '167', '168', '169', '170', 
    '171', '172', '173', '174', '175', '176', '177', '178', '179', '180', 
    '181', '182', '183', '184', '185', '186', '187', '188', '189', '190', 
    '191', '192', '193', '194', '195', '196', '197', '198', '199', '200', 
    '201', '202', '203', '204', '205', '206', '207', '208', '209', '210', 
    '211', '212', '213', '214', '215', '216', '217', '218', '219', '220', 
    '221', '222', '223', '224', '225', '226', '227', '228', '229', '230', 
    '231', '232', '233', '234', '235', '236', '237', '238', '239', '240', 
    '241', '242', '243', '244', '245', '246', '247', '248', '249', '250', 
    '251', '252', '253', '254', '255', '256', '257', '258', '259', '260', 
    '261', '262', '263', '264', '265', '266', '267', '268', '269', '270', 
    '271', '272', '273', '274', '275', '276', '277', '278', '279', '280', 
    '281', '282', '283', '284', '285', '286', '287', '288', '289', '290', 
    '291', '292', '293', '294', '295', '296', '297', '298', '299', '300', 
    '301', '302', '303', '304', '305', '306', '307', '308']


# Compression-specific constants
QP1 = [5, 10, 16, 20, 24, 27, 32, 39, 42, 45]
QP2 = [10, 15, 20, 25, 30, 32, 35, 40, 45, 50]
QP3 = [10, 15, 20, 25, 30, 32, 35, 40, 45, 50]


CTU = [64]
PRESET = ['medium']

def single_iterator():
    for f in FILE_NAME:
        for q1 in QP1:
            for c in CTU:
                for p in PRESET:
                    yield f, q1, c, p

def second_iterator():
    for f in FILE_NAME:
        for q1 in QP1:
            for q2 in QP2:
                for c in CTU:
                    for p in PRESET:
                        yield f, q1, q2, c, p
                        
def triple_iterator():
    for f in FILE_NAME:
        for q1 in QP1:
            for q2 in QP2:
                for q3 in QP3:
                    for c in CTU:
                        for p in PRESET:
                            yield f, q1, q2, q3, c, p
                            
                            
                

def get_single_file_name(file_name, QP1, CTU, PRESET):
    return f"{file_name}_1stQP{QP1}_CTU{CTU}_PRESET{PRESET}.heif"

def get_second_file_name(file_name, QP1, QP2, CTU, PRESET):
    return f"{file_name}_1stQP{QP1}_2ndQP{QP2}_CTU{CTU}_PRESET{PRESET}.heif"

def get_triple_file_name(file_name, QP1, QP2, QP3, CTU, PRESET):
    return f"{file_name}_1stQP{QP1}_2ndQP{QP2}_3rdQP{QP3}_CTU{CTU}_PRESET{PRESET}.heif"



def get_single_265_name(file_name, QP1, CTU, PRESET):
    return f"{file_name}_1stQP{QP1}_CTU{CTU}_PRESET{PRESET}.265"

def get_second_265_name(file_name, QP1, QP2, CTU, PRESET):
    return f"{file_name}_1stQP{QP1}_2ndQP{QP2}_CTU{CTU}_PRESET{PRESET}.265"

def get_triple_265_name(file_name, QP1, QP2, QP3, CTU, PRESET):
    return f"{file_name}_1stQP{QP1}_2ndQP{QP2}_3rdQP{QP3}_CTU{CTU}_PRESET{PRESET}.265"



def get_single_265_name2(file_name, QP1, CTU, PRESET):
    return f"{file_name}_1stQP{QP1}_CTU{CTU}_PRESET{PRESET}_master1.265"

def get_second_265_name2(file_name, QP1, QP2, CTU, PRESET):
    return f"{file_name}_1stQP{QP1}_2ndQP{QP2}_CTU{CTU}_PRESET{PRESET}_master1.265"

def get_triple_265_name2(file_name, QP1, QP2, QP3, CTU, PRESET):
    return f"{file_name}_1stQP{QP1}_2ndQP{QP2}_3rdQP{QP3}_CTU{CTU}_PRESET{PRESET}_master1.265"



def get_single_csv_name(file_name, QP1, CTU, PRESET):
    return f"{file_name}_1stQP{QP1}_CTU{CTU}_PRESET{PRESET}.csv"

def get_second_csv_name(file_name, QP1, QP2, CTU, PRESET):
    return f"{file_name}_1stQP{QP1}_2ndQP{QP2}_CTU{CTU}_PRESET{PRESET}.csv"

def get_triple_csv_name(file_name, QP1, QP2, QP3, CTU, PRESET):
    return f"{file_name}_1stQP{QP1}_2ndQP{QP2}_3rdQP{QP3}_CTU{CTU}_PRESET{PRESET}.csv"



def get_single_265(file_name, QP1, CTU, PRESET):
    return f"{file_name}_1stQP{QP1}_CTU{CTU}_PRESET{PRESET}"

def get_second_265(file_name, QP1, QP2, CTU, PRESET):
    return f"{file_name}_1stQP{QP1}_2ndQP{QP2}_CTU{CTU}_PRESET{PRESET}"

def get_triple_265(file_name, QP1, QP2, QP3, CTU, PRESET):
    return f"{file_name}_1stQP{QP1}_2ndQP{QP2}_3rdQP{QP3}_CTU{CTU}_PRESET{PRESET}"



def get_single_265_data(file_name, QP1, CTU, PRESET):
    return f"{file_name}_1stQP{QP1}_CTU{CTU}_PRESET{PRESET}.npz"

def get_second_265_data(file_name, QP1, QP2, CTU, PRESET):
    return f"{file_name}_1stQP{QP1}_2ndQP{QP2}_CTU{CTU}_PRESET{PRESET}.npz"

def get_triple_265_data(file_name, QP1, QP2, QP3, CTU, PRESET):
    return f"{file_name}_1stQP{QP1}_2ndQP{QP2}_3rdQP{QP3}_CTU{CTU}_PRESET{PRESET}.npz"



def get_single_265_pkl(file_name, QP1, CTU, PRESET):
    return f"{file_name}_1stQP{QP1}_CTU{CTU}_PRESET{PRESET}.pkl"

def get_second_265_pkl(file_name, QP1, QP2, CTU, PRESET):
    return f"{file_name}_1stQP{QP1}_2ndQP{QP2}_CTU{CTU}_PRESET{PRESET}.pkl"

def get_triple_265_pkl(file_name, QP1, QP2, QP3, CTU, PRESET):
    return f"{file_name}_1stQP{QP1}_2ndQP{QP2}_3rdQP{QP3}_CTU{CTU}_PRESET{PRESET}.pkl"



def get_single_265_data_D(file_name, QP1, CTU, PRESET):
    return f"{file_name}_1stQP{QP1}_CTU{CTU}_PRESET{PRESET}_cu_depth.dat"

def get_second_265_data_D(file_name, QP1, QP2, CTU, PRESET):
    return f"{file_name}_1stQP{QP1}_2ndQP{QP2}_CTU{CTU}_PRESET{PRESET}_cu_depth.dat"

def get_triple_265_data_D(file_name, QP1, QP2, QP3, CTU, PRESET):
    return f"{file_name}_1stQP{QP1}_2ndQP{QP2}_3rdQP{QP3}_CTU{CTU}_PRESET{PRESET}_cu_depth.dat"



def get_single_265_data_P(file_name, QP1, CTU, PRESET):
    return f"{file_name}_1stQP{QP1}_CTU{CTU}_PRESET{PRESET}_cu_pu.dat"

def get_second_265_data_P(file_name, QP1, QP2, CTU, PRESET):
    return f"{file_name}_1stQP{QP1}_2ndQP{QP2}_CTU{CTU}_PRESET{PRESET}_cu_pu.dat"

def get_triple_265_data_P(file_name, QP1, QP2, QP3, CTU, PRESET):
    return f"{file_name}_1stQP{QP1}_2ndQP{QP2}_3rdQP{QP3}_CTU{CTU}_PRESET{PRESET}_cu_pu.dat"



def get_single_265_data_L(file_name, QP1, CTU, PRESET):
    return f"{file_name}_1stQP{QP1}_CTU{CTU}_PRESET{PRESET}_cu_intradir_L.dat"

def get_second_265_data_L(file_name, QP1, QP2, CTU, PRESET):
    return f"{file_name}_1stQP{QP1}_2ndQP{QP2}_CTU{CTU}_PRESET{PRESET}_cu_intradir_L.dat"

def get_triple_265_data_L(file_name, QP1, QP2, QP3, CTU, PRESET):
    return f"{file_name}_1stQP{QP1}_2ndQP{QP2}_3rdQP{QP3}_CTU{CTU}_PRESET{PRESET}_cu_intradir_L.dat"



def get_single_265_data_C(file_name, QP1, CTU, PRESET):
    return f"{file_name}_1stQP{QP1}_CTU{CTU}_PRESET{PRESET}_cu_intradir_C.dat"

def get_second_265_data_C(file_name, QP1, QP2, CTU, PRESET):
    return f"{file_name}_1stQP{QP1}_2ndQP{QP2}_CTU{CTU}_PRESET{PRESET}_cu_intradir_C.dat"

def get_triple_265_data_C(file_name, QP1, QP2, QP3, CTU, PRESET):
    return f"{file_name}_1stQP{QP1}_2ndQP{QP2}_3rdQP{QP3}_CTU{CTU}_PRESET{PRESET}_cu_intradir_C.dat"



def get_single_265_data_Q(file_name, QP1, CTU, PRESET):
    return f"{file_name}_1stQP{QP1}_CTU{CTU}_PRESET{PRESET}_cu_qp.dat"

def get_second_265_data_Q(file_name, QP1, QP2, CTU, PRESET):
    return f"{file_name}_1stQP{QP1}_2ndQP{QP2}_CTU{CTU}_PRESET{PRESET}_cu_qp.dat"

def get_triple_265_data_Q(file_name, QP1, QP2, QP3, CTU, PRESET):
    return f"{file_name}_1stQP{QP1}_2ndQP{QP2}_3rdQP{QP3}_CTU{CTU}_PRESET{PRESET}_cu_qp.dat"



def get_single_combined_data(file_name, QP1, CTU, PRESET):
    return f"{file_name}_1stQP{QP1}_CTU{CTU}_PRESET{PRESET}.csv"

def get_second_combined_data(file_name, QP1, QP2, CTU, PRESET):
    return f"{file_name}_1stQP{QP1}_2ndQP{QP2}_CTU{CTU}_PRESET{PRESET}.csv"

def get_triple_combined_data(file_name, QP1, QP2, QP3, CTU, PRESET):
    return f"{file_name}_1stQP{QP1}_2ndQP{QP2}_3rdQP{QP3}_CTU{CTU}_PRESET{PRESET}.csv"

