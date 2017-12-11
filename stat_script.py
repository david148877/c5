import os
import numpy as np

#clock = clock_pool[0]
#l1d_assoc = l1d_assoc_pool[0]
#l1d_size = l1d_size_pool[0]

# key_words={'num_inst':'system.cpu.committedInsts',\
#            'ave_gap':'system.mem_ctrl.avgGap',\
#            'dcache_hits':'system.cpu.dcache.overall_hits::total',\
#            'l1_num_replace':'system.cpu.dcache.tags.replacements',\
#            'dcache_miss_rate':'system.cpu.dcache.overall_miss_rate::total',\
#            'icache_miss_rate':'system.cpu.icache.overall_miss_rate::total',\
#            'l2cache_miss_rate':'system.l2Cache.overall_miss_rate::total',\
#            'num_cycles':'system.cpu.numCycles'}

key_words={'nb_of_sec':'sim_seconds',\
           'nb_of_float_lookups':'system.cpu.rename.fp_rename_lookups',\
           'iq_rate':'system.cpu.iq.rate',\
           'cycs_of_register':'system.cpu.rename.RenameLookups',\
           'nb_of_times_ROB':'system.cpu.rename.ROBFullEvents',\
           'dcache_miss_rate':'system.cpu.dcache.overall_miss_rate::total',\
           'icache_miss_rate':'system.cpu.icache.overall_miss_rate::total',\
           'l2cache_miss_rate':'system.l2.overall_miss_rate::total'}
           
result_file = 'm5out/stats.txt'

# i = 0
# j = 0
# k =0

nb_fp = 64
nb_iq = 4
nb_bf = 4

nb_fp_sweep = 6
nb_iq_sweep = 7
nb_bf_sweep = 7
nb_record = 8
stat_dir = os.path.expanduser('/home/warehouse/pohsuchen/cse560m/configs/m5out')
hw3_dir = os.path.expanduser('/home/warehouse/pohsuchen/cse560m/configs')
save_record_dir = os.path.expanduser('/home/warehouse/pohsuchen/cse560m/configs/m5out')

if os.path.exists(save_record_dir) == False:
	os.mkdir(save_record_dir)

record_list = []
for i in range(nb_fp_sweep):
	for j in range(nb_iq_sweep):
		for k in range(nb_bf_sweep):
			# stat_file_path = os.path.join(stat_dir,'{}_{}_{}.txt'.format(nb_fp*2**i, nb_iq*2**j,nb_bf*2**k)
			stat_file_path = os.path.join(stat_dir,'stats_{}_{}_{}.txt'.format(nb_fp*2**i, nb_iq*2**j,nb_bf*2**k))
# 			stat_file_path = os.path.join(stat_dir,'{}_{}_{}.txt'.format(i, j, k))
			record = np.zeros(nb_record)
			with open(stat_file_path) as f:
				for line in f.readlines():
					str_splits = line.split()
					if len(str_splits) == 0:
						continue
					if str_splits[0] == key_words['nb_of_sec']:
						record[0] = float(str_splits[1])
						print(line)
					elif str_splits[0] == key_words['nb_of_float_lookups']:
						record[1] = float(str_splits[1])
						print(line)
					elif str_splits[0] == key_words['iq_rate']:
						record[2] = float(str_splits[1])
						print(line)
					elif str_splits[0] == key_words['cycs_of_register']:
						record[3] = float(str_splits[1])
						print(line)
					elif str_splits[0] == key_words['nb_of_times_ROB']:
						record[4] = float(str_splits[1])
						print(line)
					elif str_splits[0] == key_words['dcache_miss_rate']:
						record[5] = float(str_splits[1])
						print(line)
					elif str_splits[0] == key_words['icache_miss_rate']:
						record[6] = float(str_splits[1])
						print(line)
					elif str_splits[0] == key_words['l2cache_miss_rate']:
						record[7] = float(str_splits[1])
						print(line)
			record_list.append(record)

final_mat = np.array(record_list)
print(final_mat.shape)
# final_mat = np.transpose(record_mat,(3,0,1,2))
# mat_file_path = os.path.join(hw3_dir, 'record.mat')
# scipy.io.savemat(mat_file_path, mdict={'record': final_mat})

## save the data into matlib file
# store the results
import csv
result_csv = os.path.join(hw3_dir,'analysis_result.csv')
print(result_csv)
result_arr = final_mat.reshape(-1, nb_record)
# result_arr = np.array(record_list).reshape(len(record_list),len(record))
# result_arr_rot = result_arr.transpose()
# with open(result_csv, 'w') as csvfile:
# 	fieldnames = ['Configurations','nb_of_sec', 'nb_of_float_lookups', 'nb_of_inst_iq', 'nb_of_inst_issued', \
# 				 'cycs_of_register', 'nb_of_times_ROB', 'dcache_miss_rate', 'icache_miss_rate',\
# 				 'l2cache_miss_rate']

base_fp = 64
base_iq = 4
base_bf = 4

idx = 0
with open(result_csv, 'w') as csvfile:
	fieldnames = ['Configs','nb_of_sec', 'nb_of_float_lookups', 'iq_rate', \
				 'cycs_of_register', 'nb_of_times_ROB', 'dcache_miss_rate', 'icache_miss_rate',\
				 'l2cache_miss_rate']
	writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
	writer.writeheader()
	for i in range(nb_fp_sweep):
		for j in range(nb_iq_sweep):
			for k in range(nb_bf_sweep):
				config_str = '{},{},{}'.format(base_fp*2**i,base_iq*2**j,base_bf*2**k)
				writer.writerow({fieldnames[0]:config_str,fieldnames[1]:result_arr[idx,0], fieldnames[2]:result_arr[idx,1],
								fieldnames[3]: result_arr[idx,2], fieldnames[4]: result_arr[idx,3], fieldnames[5]: result_arr[idx,4], 
								fieldnames[6]:result_arr[idx,5],fieldnames[7]:result_arr[idx,6], fieldnames[8]:result_arr[idx,7]})
# 				print(result_arr[idx,5])
				print(result_arr[idx,:])
				idx += 1
# 				print(idx)
# 			save_result_path = os.path.join(save_record_dir,'{}_{}_{}.txt'.format(str(i),str(j),str(k)))
# 			with open(save_result_path, 'w') as f:
# 				for idx in range(nb_record):
# 					f.write(str(record[idx]))
# 					if idx < nb_record -1:
# 						f.write('\t')
