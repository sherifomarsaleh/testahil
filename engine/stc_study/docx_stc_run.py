import docx_stc_A   # masthead → §2
import docx_stc_B   # §3 → §7
import docx_stc_C   # appendices → footer + save
import os

HERE = os.path.dirname(os.path.abspath(__file__))
# Absolute against this file's own directory: the builders read and wrote relative
# to the working directory, so running them from the repository root — which is how
# every gate does — found no inputs and scattered the outputs.

