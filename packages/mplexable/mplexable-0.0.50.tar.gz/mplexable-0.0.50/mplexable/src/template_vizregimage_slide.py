########
# title: template_vizregimage_slide.py
#
# author: Jenny, bue
# license: GPLv>=3
# version: 2021-06-25
#
# description:
#     template script for python base registered image qc plot generation.
#
# instruction:
#     use mplexable.visualize_reg_images_spawn function to generate and run executable from this template.
#####

# libraries
from mplexable import _version
from mplexable import regist
import resource
import time

# set variables
poke_s_slide = 'peek_s_slide'
poke_s_color = 'peek_s_color'
poke_s_regdir = 'peek_s_regdir'
poke_s_format_regdir = 'peek_s_format_regdir'
poke_s_qcdir = 'peek_s_qcdir'

# off we go
print(f'run mplexable.regist.visualize_reg_images on {poke_s_slide} {poke_s_color} ...')
r_time_start = time.time()

# visualize registered images for qc
regist.visualize_reg_images(
    s_slide = poke_s_slide,
    s_color = poke_s_color,
    s_regdir = poke_s_regdir,
    s_format_regdir = poke_s_format_regdir,  # s_path_regdir, s_slide_pxscene
    s_qcdir = poke_s_qcdir,
)

# rock to the end
r_time_stop = time.time()
print('done mplexable.regist.visualize_reg_images!')
print(f'run time: {(r_time_stop - r_time_start) / 3600}[h]')
print(f'run max memory: {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000000}[GB]')
print('you are running mplexable version:', _version.__version__)
