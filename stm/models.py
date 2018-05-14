# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import re
import datetime


from pyMTRX import experiment

from django.db import models
from django.conf import settings
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.exceptions import ValidationError

# Create your models here.

class Operator(models.Model):
    firstname = models.CharField(max_length = 50)
    lastname = models.CharField(max_length = 50)
    email = models.EmailField(max_length = 254)

    def __unicode__(self):
        return u'{} {}'.format(self.firstname, self.lastname)

class StandardOperatingProcedure(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(max_length=5000)
    manual = models.FileField(upload_to='stm/sop/', max_length=100, verbose_name='Manual', blank=True)

    def __unicode__(self):
        return u'{}'.format(self.name)

class Sample(models.Model):
    material = models.CharField(max_length=50)
    snowball_measurement = models.ForeignKey('snowball.measurement', blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(max_length=500, blank=True)

    def __unicode__(self):
        return u'{}'.format(self.material)

class Log():
    def __init__(self):
        self.text = ''

    def write(self, message):
        self.text = self.text + '\n' + message


class Measurement(models.Model):
    STM = 'STM'
    STS = 'STS'
    STA = 'STA'
    EXPERIMENT_CHOICES = (
        (STM, 'STM'),
        (STS, 'STS'),
        (STA, 'STA'),
    )

    operator = models.ForeignKey('Operator', on_delete=models.CASCADE, default=lambda: Operator.objects.get(id=1))
    time = models.DateTimeField(auto_now = False, auto_now_add = False, blank=True)
    experiment_type = models.CharField(max_length=3, default=STM, choices=EXPERIMENT_CHOICES)
    tip_type = models.CharField(max_length=10)
    sample = models.ForeignKey('Sample')
    name = models.CharField(max_length=100, blank=True, db_index=True)

    def clean(self):
        super(Measurement, self).clean()

        if self.time is None:
            try:
                # try to parse the name as a date
                self.time = datetime.datetime.strptime(self.name, '%d-%b-%Y')
            except ValueError:
                raise ValidationError('Could not parse the name of the model as a date. Please provide a date!')

    def __unicode__(self):
        return u'{}: {}'.format(self.id, self.sample)

    def read_images(self):
        # this function reads all images from a given folder

        # sub function to create data_field names from property names
        def convert_to_data_field(field_name):
            return field_name.lower()

        path = os.path.join(settings.STM_STORAGE, self.name)
        logger = Log()

        files = os.listdir(path)
        mainfile = None
        for file in files:
            if file.find('_0001.mtrx') != -1:
                # we found the main file
                mainfile = file
                break

        if mainfile is None:
            pass # TODO: warning

        ex = experiment.Experiment(os.path.join(path, mainfile))
        image_count = 0

        # filename parsing
        filenumber_regex = '--([0-9]{1,2}_[0-9]{1,2})\.'
        regex = re.compile(filenumber_regex)

        # read all images
        for scan, _ in ex._cmnt_lkup.items():
            if 'I_mtrx' in scan or 'Z_mtrx' in scan:
                try:
                    image = ex.import_scan(os.path.join(path, scan))
                    success = True
                except:
                    success = False

                if success:
                    image_count = image_count + 1
                    image_obj = Image(measurement=self)
                    for prop, value in image[0][0].props.items():
                        try:
                            setattr(image_obj, convert_to_data_field(prop), value.value)
                        except:
                            pass # todo maybe log that

                    if 'I_mtrx' in scan:
                        image_obj.type = Image.I
                    else:
                        image_obj.type = Image.V

                    # note name
                    matches = regex.search(scan)
                    if matches is not None:
                        groups = matches.groups()
                        image_obj.name = groups[0]

                    image_obj.save()

                    # save png preview image
                    fn = NamedTemporaryFile(delete=True)
                    try:
                        image[0][0].save_png(fn.name)
                        image_obj.preview_image.save('{}.png'.format(image_obj.id), File(fn), save=True)
                    except ValueError:
                        logger.write('Image {} could not be written'.format(image_obj.id))
        return image_count

class Image(models.Model):
    I = 'I'
    V = 'V'
    Z = 'Z'
    IMAGETYPES = (
        (I, 'I'),
        (V, 'V'),
        (Z, 'Z'),
    )

    measurement = models.ForeignKey('Measurement')
    name = models.CharField(max_length=150, blank=True)
    type = models.CharField(max_length=2, choices=IMAGETYPES)
    preview_image = models.ImageField(upload_to='stm/preview_images/', blank=True, null=True)

    # autogenerated image parameters starting here
    aux1_auto_oversampling = models.NullBooleanField(verbose_name='Aux1 Auto Oversampling')
    aux1_enable = models.NullBooleanField(verbose_name='Aux1 Enable')
    aux1_enable_storing = models.NullBooleanField(verbose_name='Aux1 Enable Storing')
    aux1_initial_delay = models.FloatField(blank=True, null=True, verbose_name='Aux1 Initial Delay')
    aux1_oversampling_factor = models.FloatField(blank=True, null=True, verbose_name='Aux1 Oversampling Factor')
    aux1_v_auto_flush_period = models.FloatField(blank=True, null=True, verbose_name='Aux1 V Auto Flush Period')
    aux1_v_auto_oversampling = models.NullBooleanField(verbose_name='Aux1 V Auto Oversampling')
    aux1_v_enable = models.NullBooleanField(verbose_name='Aux1 V Enable')
    aux1_v_enable_storing = models.NullBooleanField(verbose_name='Aux1 V Enable Storing')
    aux1_v_initial_delay = models.FloatField(blank=True, null=True, verbose_name='Aux1 V Initial Delay')
    aux1_v_oversampling_factor = models.FloatField(blank=True, null=True, verbose_name='Aux1 V Oversampling Factor')
    aux1_z_auto_flush_period = models.FloatField(blank=True, null=True, verbose_name='Aux1 Z Auto Flush Period')
    aux1_z_auto_oversampling = models.NullBooleanField(verbose_name='Aux1 Z Auto Oversampling')
    aux1_z_enable = models.NullBooleanField(verbose_name='Aux1 Z Enable')
    aux1_z_enable_storing = models.NullBooleanField(verbose_name='Aux1 Z Enable Storing')
    aux1_z_initial_delay = models.FloatField(blank=True, null=True, verbose_name='Aux1 Z Initial Delay')
    aux1_z_oversampling_factor = models.FloatField(blank=True, null=True, verbose_name='Aux1 Z Oversampling Factor')
    aux2_auto_oversampling = models.NullBooleanField(verbose_name='Aux2 Auto Oversampling')
    aux2_enable = models.NullBooleanField(verbose_name='Aux2 Enable')
    aux2_enable_storing = models.NullBooleanField(verbose_name='Aux2 Enable Storing')
    aux2_initial_delay = models.FloatField(blank=True, null=True, verbose_name='Aux2 Initial Delay')
    aux2_oversampling_factor = models.FloatField(blank=True, null=True, verbose_name='Aux2 Oversampling Factor')
    aux2_t_auto_oversampling = models.NullBooleanField(verbose_name='Aux2 t Auto Oversampling')
    aux2_t_enable = models.NullBooleanField(verbose_name='Aux2 t Enable')
    aux2_t_enable_storing = models.NullBooleanField(verbose_name='Aux2 t Enable Storing')
    aux2_t_initial_delay = models.FloatField(blank=True, null=True, verbose_name='Aux2 t Initial Delay')
    aux2_t_oversampling_factor = models.FloatField(blank=True, null=True, verbose_name='Aux2 t Oversampling Factor')
    aux2_v_auto_flush_period = models.FloatField(blank=True, null=True, verbose_name='Aux2 V Auto Flush Period')
    aux2_v_auto_oversampling = models.NullBooleanField(verbose_name='Aux2 V Auto Oversampling')
    aux2_v_enable = models.NullBooleanField(verbose_name='Aux2 V Enable')
    aux2_v_enable_storing = models.NullBooleanField(verbose_name='Aux2 V Enable Storing')
    aux2_v_initial_delay = models.FloatField(blank=True, null=True, verbose_name='Aux2 V Initial Delay')
    aux2_v_oversampling_factor = models.FloatField(blank=True, null=True, verbose_name='Aux2 V Oversampling Factor')
    aux2_z_auto_flush_period = models.FloatField(blank=True, null=True, verbose_name='Aux2 Z Auto Flush Period')
    aux2_z_auto_oversampling = models.NullBooleanField(verbose_name='Aux2 Z Auto Oversampling')
    aux2_z_enable = models.NullBooleanField(verbose_name='Aux2 Z Enable')
    aux2_z_enable_storing = models.NullBooleanField(verbose_name='Aux2 Z Enable Storing')
    aux2_z_initial_delay = models.FloatField(blank=True, null=True, verbose_name='Aux2 Z Initial Delay')
    aux2_z_oversampling_factor = models.FloatField(blank=True, null=True, verbose_name='Aux2 Z Oversampling Factor')
    clock1_enable = models.NullBooleanField(verbose_name='Clock1 Enable')
    clock1_period = models.FloatField(blank=True, null=True, verbose_name='Clock1 Period')
    clock1_samples = models.FloatField(blank=True, null=True, verbose_name='Clock1 Samples')
    clock2_enable = models.NullBooleanField(verbose_name='Clock2 Enable')
    clock2_period = models.FloatField(blank=True, null=True, verbose_name='Clock2 Period')
    clock2_samples = models.FloatField(blank=True, null=True, verbose_name='Clock2 Samples')
    clock3_enable = models.NullBooleanField(verbose_name='Clock3 Enable')
    clock3_period = models.FloatField(blank=True, null=True, verbose_name='Clock3 Period')
    clock3_samples = models.FloatField(blank=True, null=True, verbose_name='Clock3 Samples')
    crtcservice_aab_mux_0 = models.FloatField(blank=True, null=True, verbose_name='CRTCService AAB Mux 0')
    crtcservice_aab_mux_1 = models.FloatField(blank=True, null=True, verbose_name='CRTCService AAB Mux 1')
    crtcservice_aab_mux_2 = models.FloatField(blank=True, null=True, verbose_name='CRTCService AAB Mux 2')
    crtcservice_aab_mux_3 = models.FloatField(blank=True, null=True, verbose_name='CRTCService AAB Mux 3')
    crtcservice_enable_pfu_filter = models.NullBooleanField(verbose_name='CRTCService Enable PFU Filter')
    crtcservice_pfu_z_gain = models.FloatField(blank=True, null=True, verbose_name='CRTCService PFU Z Gain')
    drbservice_aux1_in_select = models.FloatField(blank=True, null=True, verbose_name='DRBService Aux1 In Select')
    drbservice_aux2_in_select = models.FloatField(blank=True, null=True, verbose_name='DRBService Aux2 In Select')
    drbservice_lp_aux1_in = models.FloatField(blank=True, null=True, verbose_name='DRBService Lp Aux1 In')
    drbservice_lp_aux1_in_aa = models.NullBooleanField(verbose_name='DRBService Lp Aux1 In AA')
    drbservice_lp_aux2_in = models.FloatField(blank=True, null=True, verbose_name='DRBService Lp Aux2 In')
    drbservice_lp_aux2_in_aa = models.NullBooleanField(verbose_name='DRBService Lp Aux2 In AA')
    drbservice_lp_z_ext = models.FloatField(blank=True, null=True, verbose_name='DRBService Lp Z Ext')
    drbservice_lp_z_out = models.FloatField(blank=True, null=True, verbose_name='DRBService Lp Z Out')
    drbservice_vcal_in_select = models.FloatField(blank=True, null=True, verbose_name='DRBService VCal In Select')
    gapvoltagecontrol_alternate_preamp_range = models.CharField(max_length = 100, blank=True, verbose_name='GapVoltageControl Alternate Preamp Range (Unit: --)')
    gapvoltagecontrol_alternate_voltage = models.FloatField(blank=True, null=True, verbose_name='GapVoltageControl Alternate Voltage')
    gapvoltagecontrol_const_voltage = models.NullBooleanField(verbose_name='GapVoltageControl Const Voltage')
    gapvoltagecontrol_enable_alternate_preamp_range = models.NullBooleanField(verbose_name='GapVoltageControl Enable Alternate Preamp Range')
    gapvoltagecontrol_enable_alternate_voltage = models.NullBooleanField(verbose_name='GapVoltageControl Enable Alternate Voltage')
    gapvoltagecontrol_preamp_range = models.CharField(max_length = 100, blank=True, verbose_name='GapVoltageControl Preamp Range (Unit: --)')
    gapvoltagecontrol_tip_cond_enable_feedback_loop = models.NullBooleanField(verbose_name='GapVoltageControl Tip Cond Enable Feedback Loop')
    gapvoltagecontrol_tip_cond_pulse_preamp_range = models.CharField(max_length = 100, blank=True, verbose_name='GapVoltageControl Tip Cond Pulse Preamp Range (Unit: --)')
    gapvoltagecontrol_tip_cond_pulse_time = models.FloatField(blank=True, null=True, verbose_name='GapVoltageControl Tip Cond Pulse Time')
    gapvoltagecontrol_tip_cond_pulse_voltage = models.FloatField(blank=True, null=True, verbose_name='GapVoltageControl Tip Cond Pulse Voltage')
    gapvoltagecontrol_voltage = models.FloatField(blank=True, null=True, verbose_name='GapVoltageControl Voltage')
    i_auto_oversampling = models.NullBooleanField(verbose_name='I Auto Oversampling')
    i_enable = models.NullBooleanField(verbose_name='I Enable')
    i_enable_storing = models.NullBooleanField(verbose_name='I Enable Storing')
    i_initial_delay = models.FloatField(blank=True, null=True, verbose_name='I Initial Delay')
    i_oversampling_factor = models.FloatField(blank=True, null=True, verbose_name='I Oversampling Factor')
    i_reg_auto_oversampling = models.NullBooleanField(verbose_name='I Reg Auto Oversampling')
    i_reg_enable = models.NullBooleanField(verbose_name='I Reg Enable')
    i_reg_enable_storing = models.NullBooleanField(verbose_name='I Reg Enable Storing')
    i_reg_initial_delay = models.FloatField(blank=True, null=True, verbose_name='I Reg Initial Delay')
    i_reg_oversampling_factor = models.FloatField(blank=True, null=True, verbose_name='I Reg Oversampling Factor')
    i_t_auto_oversampling = models.NullBooleanField(verbose_name='I t Auto Oversampling')
    i_t_enable = models.NullBooleanField(verbose_name='I t Enable')
    i_t_enable_storing = models.NullBooleanField(verbose_name='I t Enable Storing')
    i_t_initial_delay = models.FloatField(blank=True, null=True, verbose_name='I t Initial Delay')
    i_t_oversampling_factor = models.FloatField(blank=True, null=True, verbose_name='I t Oversampling Factor')
    i_v_auto_flush_period = models.FloatField(blank=True, null=True, verbose_name='I V Auto Flush Period')
    i_v_auto_oversampling = models.NullBooleanField(verbose_name='I V Auto Oversampling')
    i_v_enable = models.NullBooleanField(verbose_name='I V Enable')
    i_v_enable_storing = models.NullBooleanField(verbose_name='I V Enable Storing')
    i_v_initial_delay = models.FloatField(blank=True, null=True, verbose_name='I V Initial Delay')
    i_v_oversampling_factor = models.FloatField(blank=True, null=True, verbose_name='I V Oversampling Factor')
    i_z_auto_flush_period = models.FloatField(blank=True, null=True, verbose_name='I Z Auto Flush Period')
    i_z_auto_oversampling = models.NullBooleanField(verbose_name='I Z Auto Oversampling')
    i_z_enable = models.NullBooleanField(verbose_name='I Z Enable')
    i_z_enable_storing = models.NullBooleanField(verbose_name='I Z Enable Storing')
    i_z_initial_delay = models.FloatField(blank=True, null=True, verbose_name='I Z Initial Delay')
    i_z_oversampling_factor = models.FloatField(blank=True, null=True, verbose_name='I Z Oversampling Factor')
    regulator_adc_read_mode_1 = models.FloatField(blank=True, null=True, verbose_name='Regulator ADC Read Mode 1')
    regulator_adc_read_mode_2 = models.FloatField(blank=True, null=True, verbose_name='Regulator ADC Read Mode 2')
    regulator_algorithm_characteristics_1 = models.FloatField(blank=True, null=True, verbose_name='Regulator Algorithm Characteristics 1')
    regulator_algorithm_characteristics_2 = models.FloatField(blank=True, null=True, verbose_name='Regulator Algorithm Characteristics 2')
    regulator_alternate_line_weighting = models.FloatField(blank=True, null=True, verbose_name='Regulator Alternate Line Weighting')
    regulator_alternate_loop_gain_1_d = models.FloatField(blank=True, null=True, verbose_name='Regulator Alternate Loop Gain 1 D')
    regulator_alternate_loop_gain_1_i = models.FloatField(blank=True, null=True, verbose_name='Regulator Alternate Loop Gain 1 I')
    regulator_alternate_loop_gain_1_k = models.FloatField(blank=True, null=True, verbose_name='Regulator Alternate Loop Gain 1 K')
    regulator_alternate_loop_gain_1_p = models.FloatField(blank=True, null=True, verbose_name='Regulator Alternate Loop Gain 1 P')
    regulator_alternate_loop_gain_2_d = models.FloatField(blank=True, null=True, verbose_name='Regulator Alternate Loop Gain 2 D')
    regulator_alternate_loop_gain_2_i = models.FloatField(blank=True, null=True, verbose_name='Regulator Alternate Loop Gain 2 I')
    regulator_alternate_loop_gain_2_k = models.FloatField(blank=True, null=True, verbose_name='Regulator Alternate Loop Gain 2 K')
    regulator_alternate_loop_gain_2_p = models.FloatField(blank=True, null=True, verbose_name='Regulator Alternate Loop Gain 2 P')
    regulator_alternate_setpoint_1 = models.FloatField(blank=True, null=True, verbose_name='Regulator Alternate Setpoint 1')
    regulator_alternate_setpoint_2 = models.FloatField(blank=True, null=True, verbose_name='Regulator Alternate Setpoint 2')
    regulator_auto_approach_mode_1 = models.FloatField(blank=True, null=True, verbose_name='Regulator Auto Approach Mode 1')
    regulator_auto_approach_mode_2 = models.FloatField(blank=True, null=True, verbose_name='Regulator Auto Approach Mode 2')
    regulator_auto_approach_post_ramp_delay = models.FloatField(blank=True, null=True, verbose_name='Regulator Auto Approach Post Ramp Delay')
    regulator_auto_approach_pre_ramp_delay = models.FloatField(blank=True, null=True, verbose_name='Regulator Auto Approach Pre Ramp Delay')
    regulator_auto_approach_ramp_speed_high_range = models.FloatField(blank=True, null=True, verbose_name='Regulator Auto Approach Ramp Speed High Range')
    regulator_auto_approach_ramp_speed_low_range = models.FloatField(blank=True, null=True, verbose_name='Regulator Auto Approach Ramp Speed Low Range')
    regulator_auto_approach_retraction_speed = models.FloatField(blank=True, null=True, verbose_name='Regulator Auto Approach Retraction Speed')
    regulator_auto_approach_timeout = models.FloatField(blank=True, null=True, verbose_name='Regulator Auto Approach Timeout')
    regulator_const_setpoint = models.NullBooleanField(verbose_name='Regulator Const Setpoint')
    regulator_delta_f_min_1 = models.FloatField(blank=True, null=True, verbose_name='Regulator Delta f Min 1')
    regulator_delta_f_min_2 = models.FloatField(blank=True, null=True, verbose_name='Regulator Delta f Min 2')
    regulator_enable_alternate_line_weighting = models.NullBooleanField(verbose_name='Regulator Enable Alternate Line Weighting')
    regulator_enable_alternate_loop_gain_1_d = models.NullBooleanField(verbose_name='Regulator Enable Alternate Loop Gain 1 D')
    regulator_enable_alternate_loop_gain_1_i = models.NullBooleanField(verbose_name='Regulator Enable Alternate Loop Gain 1 I')
    regulator_enable_alternate_loop_gain_1_k = models.NullBooleanField(verbose_name='Regulator Enable Alternate Loop Gain 1 K')
    regulator_enable_alternate_loop_gain_1_p = models.NullBooleanField(verbose_name='Regulator Enable Alternate Loop Gain 1 P')
    regulator_enable_alternate_loop_gain_2_d = models.NullBooleanField(verbose_name='Regulator Enable Alternate Loop Gain 2 D')
    regulator_enable_alternate_loop_gain_2_i = models.NullBooleanField(verbose_name='Regulator Enable Alternate Loop Gain 2 I')
    regulator_enable_alternate_loop_gain_2_k = models.NullBooleanField(verbose_name='Regulator Enable Alternate Loop Gain 2 K')
    regulator_enable_alternate_loop_gain_2_p = models.NullBooleanField(verbose_name='Regulator Enable Alternate Loop Gain 2 P')
    regulator_enable_alternate_setpoint_1 = models.NullBooleanField(verbose_name='Regulator Enable Alternate Setpoint 1')
    regulator_enable_alternate_setpoint_2 = models.NullBooleanField(verbose_name='Regulator Enable Alternate Setpoint 2')
    regulator_enable_z_offset_slew_rate = models.NullBooleanField(verbose_name='Regulator Enable Z Offset Slew Rate')
    regulator_enable_z_offset_special_slew_rate = models.NullBooleanField(verbose_name='Regulator Enable Z Offset Special Slew Rate')
    regulator_enable_z_ramp_gap_voltage = models.NullBooleanField(verbose_name='Regulator Enable Z Ramp Gap Voltage')
    regulator_enable_z_ramp_slew_rate = models.NullBooleanField(verbose_name='Regulator Enable Z Ramp Slew Rate')
    regulator_feedback_loop_characteristic_1 = models.FloatField(blank=True, null=True, verbose_name='Regulator Feedback Loop Characteristic 1')
    regulator_feedback_loop_characteristic_2 = models.FloatField(blank=True, null=True, verbose_name='Regulator Feedback Loop Characteristic 2')
    regulator_feedback_loop_enabled = models.NullBooleanField(verbose_name='Regulator Feedback Loop Enabled')
    regulator_line_weighting = models.FloatField(blank=True, null=True, verbose_name='Regulator Line Weighting')
    regulator_loop_gain_1_d = models.FloatField(blank=True, null=True, verbose_name='Regulator Loop Gain 1 D')
    regulator_loop_gain_1_i = models.FloatField(blank=True, null=True, verbose_name='Regulator Loop Gain 1 I')
    regulator_loop_gain_1_k = models.FloatField(blank=True, null=True, verbose_name='Regulator Loop Gain 1 K')
    regulator_loop_gain_1_p = models.FloatField(blank=True, null=True, verbose_name='Regulator Loop Gain 1 P')
    regulator_loop_gain_2_d = models.FloatField(blank=True, null=True, verbose_name='Regulator Loop Gain 2 D')
    regulator_loop_gain_2_i = models.FloatField(blank=True, null=True, verbose_name='Regulator Loop Gain 2 I')
    regulator_loop_gain_2_k = models.FloatField(blank=True, null=True, verbose_name='Regulator Loop Gain 2 K')
    regulator_loop_gain_2_p = models.FloatField(blank=True, null=True, verbose_name='Regulator Loop Gain 2 P')
    regulator_preamp_range_1 = models.CharField(max_length = 100, blank=True, verbose_name='Regulator Preamp Range 1 (Unit: --)')
    regulator_preamp_range_2 = models.CharField(max_length = 100, blank=True, verbose_name='Regulator Preamp Range 2 (Unit: --)')
    regulator_retraction_speed = models.FloatField(blank=True, null=True, verbose_name='Regulator Retraction Speed')
    regulator_run_frequency = models.FloatField(blank=True, null=True, verbose_name='Regulator Run Frequency')
    regulator_setpoint_1 = models.FloatField(blank=True, null=True, verbose_name='Regulator Setpoint 1')
    regulator_setpoint_2 = models.FloatField(blank=True, null=True, verbose_name='Regulator Setpoint 2')
    regulator_setpoint_limit_absolute_1 = models.FloatField(blank=True, null=True, verbose_name='Regulator Setpoint Limit Absolute 1')
    regulator_setpoint_limit_absolute_2 = models.FloatField(blank=True, null=True, verbose_name='Regulator Setpoint Limit Absolute 2')
    regulator_sign_1 = models.FloatField(blank=True, null=True, verbose_name='Regulator Sign 1')
    regulator_sign_2 = models.FloatField(blank=True, null=True, verbose_name='Regulator Sign 2')
    regulator_special_line_weighting = models.FloatField(blank=True, null=True, verbose_name='Regulator Special Line Weighting')
    regulator_special_loop_gain_1_d = models.FloatField(blank=True, null=True, verbose_name='Regulator Special Loop Gain 1 D')
    regulator_special_loop_gain_1_i = models.FloatField(blank=True, null=True, verbose_name='Regulator Special Loop Gain 1 I')
    regulator_special_loop_gain_1_k = models.FloatField(blank=True, null=True, verbose_name='Regulator Special Loop Gain 1 K')
    regulator_special_loop_gain_1_p = models.FloatField(blank=True, null=True, verbose_name='Regulator Special Loop Gain 1 P')
    regulator_special_loop_gain_2_d = models.FloatField(blank=True, null=True, verbose_name='Regulator Special Loop Gain 2 D')
    regulator_special_loop_gain_2_i = models.FloatField(blank=True, null=True, verbose_name='Regulator Special Loop Gain 2 I')
    regulator_special_loop_gain_2_k = models.FloatField(blank=True, null=True, verbose_name='Regulator Special Loop Gain 2 K')
    regulator_special_loop_gain_2_p = models.FloatField(blank=True, null=True, verbose_name='Regulator Special Loop Gain 2 P')
    regulator_special_preamp_range_1 = models.CharField(max_length = 100, blank=True, verbose_name='Regulator Special Preamp Range 1 (Unit: --)')
    regulator_special_preamp_range_2 = models.CharField(max_length = 100, blank=True, verbose_name='Regulator Special Preamp Range 2 (Unit: --)')
    regulator_special_setpoint_1 = models.FloatField(blank=True, null=True, verbose_name='Regulator Special Setpoint 1')
    regulator_special_setpoint_2 = models.FloatField(blank=True, null=True, verbose_name='Regulator Special Setpoint 2')
    regulator_z_offset = models.FloatField(blank=True, null=True, verbose_name='Regulator Z Offset')
    regulator_z_offset_delay = models.FloatField(blank=True, null=True, verbose_name='Regulator Z Offset Delay')
    regulator_z_offset_slew_rate = models.FloatField(blank=True, null=True, verbose_name='Regulator Z Offset Slew Rate')
    regulator_z_offset_special = models.FloatField(blank=True, null=True, verbose_name='Regulator Z Offset Special')
    regulator_z_offset_special_delay = models.FloatField(blank=True, null=True, verbose_name='Regulator Z Offset Special Delay')
    regulator_z_offset_special_slew_rate = models.FloatField(blank=True, null=True, verbose_name='Regulator Z Offset Special Slew Rate')
    regulator_z_ramp = models.FloatField(blank=True, null=True, verbose_name='Regulator Z Ramp')
    regulator_z_ramp_delay = models.FloatField(blank=True, null=True, verbose_name='Regulator Z Ramp Delay')
    regulator_z_ramp_slew_rate = models.FloatField(blank=True, null=True, verbose_name='Regulator Z Ramp Slew Rate')
    spectroscopy_alternate_aux1_range = models.CharField(max_length = 100, blank=True, verbose_name='Spectroscopy Alternate Aux1 Range (Unit: --)')
    spectroscopy_alternate_aux2_range = models.CharField(max_length = 100, blank=True, verbose_name='Spectroscopy Alternate Aux2 Range (Unit: --)')
    spectroscopy_alternate_delay_t1_1 = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Alternate Delay T1 1')
    spectroscopy_alternate_delay_t1_2 = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Alternate Delay T1 2')
    spectroscopy_alternate_delay_t2_1 = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Alternate Delay T2 1')
    spectroscopy_alternate_delay_t2_2 = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Alternate Delay T2 2')
    spectroscopy_alternate_delay_t3_1 = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Alternate Delay T3 1')
    spectroscopy_alternate_delay_t3_2 = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Alternate Delay T3 2')
    spectroscopy_alternate_delay_t4_1 = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Alternate Delay T4 1')
    spectroscopy_alternate_delay_t4_2 = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Alternate Delay T4 2')
    spectroscopy_alternate_device_1_end = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Alternate Device 1 End')
    spectroscopy_alternate_device_1_slew_rate = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Alternate Device 1 Slew Rate')
    spectroscopy_alternate_device_1_start = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Alternate Device 1 Start')
    spectroscopy_alternate_device_2_end = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Alternate Device 2 End')
    spectroscopy_alternate_device_2_slew_rate = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Alternate Device 2 Slew Rate')
    spectroscopy_alternate_device_2_start = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Alternate Device 2 Start')
    spectroscopy_alternate_modulation_vext_t1t2 = models.NullBooleanField(verbose_name='Spectroscopy Alternate Modulation VExt T1T2')
    spectroscopy_alternate_modulation_vext_t2t3 = models.NullBooleanField(verbose_name='Spectroscopy Alternate Modulation VExt T2T3')
    spectroscopy_alternate_modulation_vmod_t1t2 = models.NullBooleanField(verbose_name='Spectroscopy Alternate Modulation VMod T1T2')
    spectroscopy_alternate_modulation_vmod_t2t3 = models.NullBooleanField(verbose_name='Spectroscopy Alternate Modulation VMod T2T3')
    spectroscopy_alternate_modulation_zext_t1t2 = models.NullBooleanField(verbose_name='Spectroscopy Alternate Modulation ZExt T1T2')
    spectroscopy_alternate_modulation_zext_t2t3 = models.NullBooleanField(verbose_name='Spectroscopy Alternate Modulation ZExt T2T3')
    spectroscopy_alternate_spectroscopy_mode = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Alternate Spectroscopy Mode')
    spectroscopy_aux1_range = models.CharField(max_length = 100, blank=True, verbose_name='Spectroscopy Aux1 Range (Unit: --)')
    spectroscopy_aux2_range = models.CharField(max_length = 100, blank=True, verbose_name='Spectroscopy Aux2 Range (Unit: --)')
    spectroscopy_correction_strategy = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Correction Strategy')
    spectroscopy_delay_t1_1 = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Delay T1 1')
    spectroscopy_delay_t1_2 = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Delay T1 2')
    spectroscopy_delay_t2_1 = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Delay T2 1')
    spectroscopy_delay_t2_2 = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Delay T2 2')
    spectroscopy_delay_t3_1 = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Delay T3 1')
    spectroscopy_delay_t3_2 = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Delay T3 2')
    spectroscopy_delay_t4_1 = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Delay T4 1')
    spectroscopy_delay_t4_2 = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Delay T4 2')
    spectroscopy_device_1_end = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Device 1 End')
    spectroscopy_device_1_points = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Device 1 Points')
    spectroscopy_device_1_ramp_step_slew_rate = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Device 1 Ramp Step Slew Rate')
    spectroscopy_device_1_repetitions = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Device 1 Repetitions')
    spectroscopy_device_1_slew_rate = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Device 1 Slew Rate')
    spectroscopy_device_1_start = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Device 1 Start')
    spectroscopy_device_2_change_negative = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Device 2 Change Negative')
    spectroscopy_device_2_change_positive = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Device 2 Change Positive')
    spectroscopy_device_2_end = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Device 2 End')
    spectroscopy_device_2_offset = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Device 2 Offset')
    spectroscopy_device_2_offset_delay = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Device 2 Offset Delay')
    spectroscopy_device_2_points = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Device 2 Points')
    spectroscopy_device_2_ramp_step_slew_rate = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Device 2 Ramp Step Slew Rate')
    spectroscopy_device_2_repetitions = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Device 2 Repetitions')
    spectroscopy_device_2_slew_rate = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Device 2 Slew Rate')
    spectroscopy_device_2_start = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Device 2 Start')
    spectroscopy_disable_feedback_loop = models.NullBooleanField(verbose_name='Spectroscopy Disable Feedback Loop')
    spectroscopy_enable_alternate_aux1_range = models.NullBooleanField(verbose_name='Spectroscopy Enable Alternate Aux1 Range')
    spectroscopy_enable_alternate_aux2_range = models.NullBooleanField(verbose_name='Spectroscopy Enable Alternate Aux2 Range')
    spectroscopy_enable_alternate_delay_t1_1 = models.NullBooleanField(verbose_name='Spectroscopy Enable Alternate Delay T1 1')
    spectroscopy_enable_alternate_delay_t1_2 = models.NullBooleanField(verbose_name='Spectroscopy Enable Alternate Delay T1 2')
    spectroscopy_enable_alternate_delay_t2_1 = models.NullBooleanField(verbose_name='Spectroscopy Enable Alternate Delay T2 1')
    spectroscopy_enable_alternate_delay_t2_2 = models.NullBooleanField(verbose_name='Spectroscopy Enable Alternate Delay T2 2')
    spectroscopy_enable_alternate_delay_t3_1 = models.NullBooleanField(verbose_name='Spectroscopy Enable Alternate Delay T3 1')
    spectroscopy_enable_alternate_delay_t3_2 = models.NullBooleanField(verbose_name='Spectroscopy Enable Alternate Delay T3 2')
    spectroscopy_enable_alternate_delay_t4_1 = models.NullBooleanField(verbose_name='Spectroscopy Enable Alternate Delay T4 1')
    spectroscopy_enable_alternate_delay_t4_2 = models.NullBooleanField(verbose_name='Spectroscopy Enable Alternate Delay T4 2')
    spectroscopy_enable_alternate_device_1_end = models.NullBooleanField(verbose_name='Spectroscopy Enable Alternate Device 1 End')
    spectroscopy_enable_alternate_device_1_slew_rate = models.NullBooleanField(verbose_name='Spectroscopy Enable Alternate Device 1 Slew Rate')
    spectroscopy_enable_alternate_device_1_start = models.NullBooleanField(verbose_name='Spectroscopy Enable Alternate Device 1 Start')
    spectroscopy_enable_alternate_device_2_end = models.NullBooleanField(verbose_name='Spectroscopy Enable Alternate Device 2 End')
    spectroscopy_enable_alternate_device_2_slew_rate = models.NullBooleanField(verbose_name='Spectroscopy Enable Alternate Device 2 Slew Rate')
    spectroscopy_enable_alternate_device_2_start = models.NullBooleanField(verbose_name='Spectroscopy Enable Alternate Device 2 Start')
    spectroscopy_enable_alternate_modulation_vext_t1t2 = models.NullBooleanField(verbose_name='Spectroscopy Enable Alternate Modulation VExt T1T2')
    spectroscopy_enable_alternate_modulation_vext_t2t3 = models.NullBooleanField(verbose_name='Spectroscopy Enable Alternate Modulation VExt T2T3')
    spectroscopy_enable_alternate_modulation_vmod_t1t2 = models.NullBooleanField(verbose_name='Spectroscopy Enable Alternate Modulation VMod T1T2')
    spectroscopy_enable_alternate_modulation_vmod_t2t3 = models.NullBooleanField(verbose_name='Spectroscopy Enable Alternate Modulation VMod T2T3')
    spectroscopy_enable_alternate_modulation_zext_t1t2 = models.NullBooleanField(verbose_name='Spectroscopy Enable Alternate Modulation ZExt T1T2')
    spectroscopy_enable_alternate_modulation_zext_t2t3 = models.NullBooleanField(verbose_name='Spectroscopy Enable Alternate Modulation ZExt T2T3')
    spectroscopy_enable_alternate_spectroscopy_mode = models.NullBooleanField(verbose_name='Spectroscopy Enable Alternate Spectroscopy Mode')
    spectroscopy_enable_device_1_ramp_reversal = models.NullBooleanField(verbose_name='Spectroscopy Enable Device 1 Ramp Reversal')
    spectroscopy_enable_device_1_ramp_step_slew_rate = models.NullBooleanField(verbose_name='Spectroscopy Enable Device 1 Ramp Step Slew Rate')
    spectroscopy_enable_device_1_slew_rate = models.NullBooleanField(verbose_name='Spectroscopy Enable Device 1 Slew Rate')
    spectroscopy_enable_device_2_ramp_reversal = models.NullBooleanField(verbose_name='Spectroscopy Enable Device 2 Ramp Reversal')
    spectroscopy_enable_device_2_ramp_step_slew_rate = models.NullBooleanField(verbose_name='Spectroscopy Enable Device 2 Ramp Step Slew Rate')
    spectroscopy_enable_device_2_slew_rate = models.NullBooleanField(verbose_name='Spectroscopy Enable Device 2 Slew Rate')
    spectroscopy_enable_gap_preset = models.NullBooleanField(verbose_name='Spectroscopy Enable Gap Preset')
    spectroscopy_enable_gap_voltage_preset_slew_rate = models.NullBooleanField(verbose_name='Spectroscopy Enable Gap Voltage Preset Slew Rate')
    spectroscopy_enable_mode_locks = models.NullBooleanField(verbose_name='Spectroscopy Enable Mode Locks')
    spectroscopy_enable_modulation = models.NullBooleanField(verbose_name='Spectroscopy Enable Modulation')
    spectroscopy_enable_status_signals = models.NullBooleanField(verbose_name='Spectroscopy Enable Status Signals')
    spectroscopy_gap_preset_feedback_post_delay = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Gap Preset Feedback Post Delay')
    spectroscopy_gap_preset_feedback_pre_delay = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Gap Preset Feedback Pre Delay')
    spectroscopy_gap_preset_mode = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Gap Preset Mode')
    spectroscopy_gap_voltage_preset = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Gap Voltage Preset')
    spectroscopy_gap_voltage_preset_range = models.CharField(max_length = 100, blank=True, verbose_name='Spectroscopy Gap Voltage Preset Range (Unit: --)')
    spectroscopy_gap_voltage_preset_slew_rate = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Gap Voltage Preset Slew Rate')
    spectroscopy_maximum_points_1 = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Maximum Points 1')
    spectroscopy_maximum_points_2 = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Maximum Points 2')
    spectroscopy_modulation_vext_t1t2 = models.NullBooleanField(verbose_name='Spectroscopy Modulation VExt T1T2')
    spectroscopy_modulation_vext_t2t3 = models.NullBooleanField(verbose_name='Spectroscopy Modulation VExt T2T3')
    spectroscopy_modulation_vmod_t1t2 = models.NullBooleanField(verbose_name='Spectroscopy Modulation VMod T1T2')
    spectroscopy_modulation_vmod_t2t3 = models.NullBooleanField(verbose_name='Spectroscopy Modulation VMod T2T3')
    spectroscopy_modulation_zext_t1t2 = models.NullBooleanField(verbose_name='Spectroscopy Modulation ZExt T1T2')
    spectroscopy_modulation_zext_t2t3 = models.NullBooleanField(verbose_name='Spectroscopy Modulation ZExt T2T3')
    spectroscopy_pause_conduct_mode = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Pause Conduct Mode')
    spectroscopy_raster_time_1 = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Raster Time 1')
    spectroscopy_raster_time_2 = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Raster Time 2')
    spectroscopy_reenable_feedback_loop = models.NullBooleanField(verbose_name='Spectroscopy Reenable Feedback Loop')
    spectroscopy_spectroscopy_mode = models.FloatField(blank=True, null=True, verbose_name='Spectroscopy Spectroscopy Mode')
    stmscbservice_it_select = models.FloatField(blank=True, null=True, verbose_name='STMSCBService IT Select')
    stmscbservice_lp_it_image_aa = models.FloatField(blank=True, null=True, verbose_name='STMSCBService Lp IT Image AA')
    stmscbservice_lp_it_regulator = models.FloatField(blank=True, null=True, verbose_name='STMSCBService Lp IT Regulator')
    stmscbservice_lp_it_regulator_aa = models.FloatField(blank=True, null=True, verbose_name='STMSCBService Lp IT Regulator AA')
    stmscbservice_lp_vgap_out_rg = models.FloatField(blank=True, null=True, verbose_name='STMSCBService Lp VGap Out Rg')
    stmscbservice_vcal_in_select = models.FloatField(blank=True, null=True, verbose_name='STMSCBService VCal In Select')
    stmscbservice_vgap_int_ext_select = models.FloatField(blank=True, null=True, verbose_name='STMSCBService VGap Int Ext Select')
    stmscbservice_vgap_out_mod_select = models.NullBooleanField(verbose_name='STMSCBService VGap Out Mod Select')
    stmscbservice_vgap_out_select = models.FloatField(blank=True, null=True, verbose_name='STMSCBService VGap Out Select')
    stmscbservice_vgap_select = models.NullBooleanField(verbose_name='STMSCBService VGap Select')
    uscbservice_adc1_in_select = models.FloatField(blank=True, null=True, verbose_name='USCBService ADC1 In Select')
    uscbservice_adc2_in_select = models.FloatField(blank=True, null=True, verbose_name='USCBService ADC2 In Select')
    uscbservice_adc3_in_select = models.FloatField(blank=True, null=True, verbose_name='USCBService ADC3 In Select')
    uscbservice_adc4_in_select = models.FloatField(blank=True, null=True, verbose_name='USCBService ADC4 In Select')
    uscbservice_dac1_cal_in_select = models.FloatField(blank=True, null=True, verbose_name='USCBService DAC1 Cal In Select')
    uscbservice_dac1_out_select = models.FloatField(blank=True, null=True, verbose_name='USCBService DAC1 Out Select')
    uscbservice_dac2_cal_in_select = models.FloatField(blank=True, null=True, verbose_name='USCBService DAC2 Cal In Select')
    uscbservice_dac2_out_select = models.FloatField(blank=True, null=True, verbose_name='USCBService DAC2 Out Select')
    uscbservice_lp_adc1_in_aa = models.FloatField(blank=True, null=True, verbose_name='USCBService Lp ADC1 In AA')
    uscbservice_lp_adc2_in_aa = models.FloatField(blank=True, null=True, verbose_name='USCBService Lp ADC2 In AA')
    uscbservice_lp_adc3_in_aa = models.FloatField(blank=True, null=True, verbose_name='USCBService Lp ADC3 In AA')
    uscbservice_lp_adc4_in_aa = models.FloatField(blank=True, null=True, verbose_name='USCBService Lp ADC4 In AA')
    uscbservice_lp_dac1_out_rg = models.FloatField(blank=True, null=True, verbose_name='USCBService Lp DAC1 Out Rg')
    uscbservice_lp_dac2_out_rg = models.FloatField(blank=True, null=True, verbose_name='USCBService Lp DAC2 Out Rg')
    xyscanner_angle = models.FloatField(blank=True, null=True, verbose_name='XYScanner Angle')
    xyscanner_auto_disable_scan = models.NullBooleanField(verbose_name='XYScanner Auto Disable Scan')
    xyscanner_drift_compensation_ratio = models.FloatField(blank=True, null=True, verbose_name='XYScanner Drift Compensation Ratio')
    xyscanner_drift_offset_elimination_rate = models.FloatField(blank=True, null=True, verbose_name='XYScanner Drift Offset Elimination Rate')
    xyscanner_enable_automatic_drift_compensation = models.NullBooleanField(verbose_name='XYScanner Enable Automatic Drift Compensation')
    xyscanner_enable_drift_compensation = models.NullBooleanField(verbose_name='XYScanner Enable Drift Compensation')
    xyscanner_enable_scan = models.NullBooleanField(verbose_name='XYScanner Enable Scan')
    xyscanner_enable_subgrid = models.NullBooleanField(verbose_name='XYScanner Enable Subgrid')
    xyscanner_exact_match = models.NullBooleanField(verbose_name='XYScanner Exact Match')
    xyscanner_height = models.FloatField(blank=True, null=True, verbose_name='XYScanner Height')
    xyscanner_line_end_delay = models.FloatField(blank=True, null=True, verbose_name='XYScanner Line End Delay')
    xyscanner_line_start_delay = models.FloatField(blank=True, null=True, verbose_name='XYScanner Line Start Delay')
    xyscanner_lines = models.FloatField(blank=True, null=True, verbose_name='XYScanner Lines')
    xyscanner_move_raster_time = models.FloatField(blank=True, null=True, verbose_name='XYScanner Move Raster Time')
    xyscanner_move_raster_time_constrained = models.NullBooleanField(verbose_name='XYScanner Move Raster Time Constrained')
    xyscanner_points = models.FloatField(blank=True, null=True, verbose_name='XYScanner Points')
    xyscanner_points_lines_constrained = models.NullBooleanField(verbose_name='XYScanner Points Lines Constrained')
    xyscanner_raster_time = models.FloatField(blank=True, null=True, verbose_name='XYScanner Raster Time')
    xyscanner_relocation_step_limit = models.FloatField(blank=True, null=True, verbose_name='XYScanner Relocation Step Limit')
    xyscanner_relocation_time_limit = models.FloatField(blank=True, null=True, verbose_name='XYScanner Relocation Time Limit')
    xyscanner_scan_constraint = models.FloatField(blank=True, null=True, verbose_name='XYScanner Scan Constraint')
    xyscanner_speed_adaptation = models.FloatField(blank=True, null=True, verbose_name='XYScanner Speed Adaptation')
    xyscanner_subgrid_constrained = models.NullBooleanField(verbose_name='XYScanner Subgrid Constrained')
    xyscanner_subgrid_match_mode = models.FloatField(blank=True, null=True, verbose_name='XYScanner Subgrid Match Mode')
    xyscanner_subgrid_x = models.FloatField(blank=True, null=True, verbose_name='XYScanner Subgrid X')
    xyscanner_subgrid_y = models.FloatField(blank=True, null=True, verbose_name='XYScanner Subgrid Y')
    xyscanner_width = models.FloatField(blank=True, null=True, verbose_name='XYScanner Width (Volts)')
    xyscanner_width_height_constrained = models.NullBooleanField(verbose_name='XYScanner Width Height Constrained')
    xyscanner_x_drift = models.FloatField(blank=True, null=True, verbose_name='XYScanner X Drift')
    xyscanner_x_offset = models.FloatField(blank=True, null=True, verbose_name='XYScanner X Offset')
    xyscanner_x_retrace = models.NullBooleanField(verbose_name='XYScanner X Retrace')
    xyscanner_y_drift = models.FloatField(blank=True, null=True, verbose_name='XYScanner Y Drift')
    xyscanner_y_offset = models.FloatField(blank=True, null=True, verbose_name='XYScanner Y Offset')
    xyscanner_y_retrace = models.NullBooleanField(verbose_name='XYScanner Y Retrace')
    z_enable = models.NullBooleanField(verbose_name='Z Enable')
    z_enable_storing = models.NullBooleanField(verbose_name='Z Enable Storing')
    z_initial_delay = models.FloatField(blank=True, null=True, verbose_name='Z Initial Delay')
    z_oversampling_factor = models.FloatField(blank=True, null=True, verbose_name='Z Oversampling Factor')
    z_t_auto_oversampling = models.NullBooleanField(verbose_name='Z t Auto Oversampling')
    z_t_enable = models.NullBooleanField(verbose_name='Z t Enable')
    z_t_enable_storing = models.NullBooleanField(verbose_name='Z t Enable Storing')
    z_t_initial_delay = models.FloatField(blank=True, null=True, verbose_name='Z t Initial Delay')
    z_t_oversampling_factor = models.FloatField(blank=True, null=True, verbose_name='Z t Oversampling Factor')

    def __unicode__(self):
        if self.name is not None:
            return u'{} ({}-type for {})'.format(self.name, self.type, self.measurement)
        else:
            return u'{}-type for ({})'.format(self.type, self.measurement)

