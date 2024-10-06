from obspy.core import read
from plotTrigger import plot_trigger
from obspy.signal.trigger import recursive_sta_lta


data_directory = r'C:\Users\bkarr\Downloads\space_apps_2024_seismic_detection\space_apps_2024_seismic_detection\data\lunar\test\data\S12_GradeB'
test_filename = r'\xa.s12.00.mhz.1970-03-30HR00_evid00020'
mseed_file = f'{data_directory}{test_filename}.mseed'

trace = read(mseed_file)[0]
df = trace.stats.sampling_rate


cft = recursive_sta_lta(trace.data, int(453 * df), int(1510* df))
trigger_values = plot_trigger(trace, cft, 2.6, 0.4)
