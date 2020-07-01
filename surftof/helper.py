from glob import glob
from datetime import datetime, timedelta
import numpy as np
import h5py

from labbooks.settings import SURFTOF_BIGSHARE_DATA_ROOT


def import_pressure(measurement_id):
    pressures = {}
    try:
        pressure_file = glob(SURFTOF_BIGSHARE_DATA_ROOT + str(measurement_id) + "/*ressure*")[0]
        a = np.loadtxt(pressure_file, delimiter='\t',
                       dtype=[('a', '|S8'), ('b', '<f4'), ('c', '<f4'),
                              ('d', '<f4'), ('e', '<f4'), ('f', '<f4'),
                              ('g', '<f4')], skiprows=1)
        ion_source = []
        surf = []
        tof = []
        for b in a:
            ion_source.append(b[1])
            surf.append(b[2])
            tof.append(b[3])
        pressures['is'] = np.median(ion_source)
        pressures['surf'] = np.median(surf)
        pressures['tof'] = np.median(tof)
    except:
        pressures['is'] = -1
        pressures['surf'] = -1
        pressures['tof'] = -1
    return pressures


def get_temp_from_file(measurement_id):
    try:
        h5_file_name = glob("{}{}/*h5".format(SURFTOF_BIGSHARE_DATA_ROOT, int(measurement_id)))[-1]
        with h5py.File(h5_file_name, 'r') as f:
            file_start = datetime.strptime(dict(f.attrs.items())['FileCreatedTimeSTR_LOCAL'][0].decode(),
                                           "%d/%m/%Y %Hh %Mm %Ss")
            file_duration = int(
                dict(f.attrs.items())['Single Spec Duration (ms)'][0] / 1000 * len(f['SPECdata']['Intensities']))
            file_end = file_start + timedelta(seconds=file_duration)
            filenames = ["{}_temperaturePT100.csv".format(file_start.strftime("%Y-%m-%d"))]
            if file_end.date() != file_start.date():
                filenames.append("{}_temperaturePT100.csv".format(file_end.strftime("%Y-%m-%d")))

            temps = []
            for filename in filenames:
                with open(SURFTOF_BIGSHARE_DATA_ROOT + 'temperature/' + filename, 'r') as g:
                    for line in g:
                        line_time = datetime.strptime(line.strip().split(',')[0][:19], '%Y-%m-%dT%H:%M:%S')
                        if file_start < line_time < file_end:
                            temps.append(float(line.strip().split(',')[1]))
            return_value = "{:.1f} &#176;C".format(np.median(temps))
            if "nan" in return_value:
                return "-1 &#176;C"
            return return_value
    except:
        return "-1 &#176;C"


def import_pico_log_and_median(measurement_id):
    try:
        current_file = glob(SURFTOF_BIGSHARE_DATA_ROOT + str(measurement_id) + "/*Pico*")[0]
        a = []
        with open(current_file) as f:
            for line in f:
                try:
                    a.append(float(line.split(' , ')[1]))
                except (IndexError, ValueError, FloatingPointError):
                    pass
        return np.median(a)
    except:
        return -1
