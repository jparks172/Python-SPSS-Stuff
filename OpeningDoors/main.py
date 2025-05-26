# Saves time writing multiple SPSS scripts and copies them to paste into SPSS syntax file
import pyperclip


def clear_clipboard():
    pyperclip.copy('')


# Outputs SPSS scripts of ancova by group for a list of specified variables over a specified time length
def output_ancova_scripts(time, var_prefixes, covariate_time):
    output = ''
    # Loops through vars for ancova runs
    for var in var_prefixes:
        # Loops through the time range specified outputs the ancova call for each time
        for i in range(time):
            output += (f"UNIANOVA {var}.{i + 2} by group WITH {var}.{covariate_time}\n"
                       f"/METHOD=SSTYPE(3)\n"
                       f"/INTERCEPT=INCLUDE\n"
                       f"/PRINT ETASQ DESCRIPTIVE\n"
                       f"/CRITERIA=ALPHA(.05)\n"
                       f"/DESIGN={var}.{covariate_time} group.\n\n")
        output += '\n'
    # Copies current clipboard and new output to be pasted into SPSS syntax file
    pyperclip.copy(pyperclip.paste() + output + 'EXECUTE.')


vars_for_measure = ['caas_total',
                    'caas_control',
                    'caas_confidence',
                    'caas_concern',
                    'caas_curiosity',
                    'basis_total',
                    'CTI_total_A',
                    'CTI_dmcSum',
                    'CTI_caSum',
                    'CTI_ecSum',
                    'whope_total',
                    'whope_agency',
                    'whope_pathways',
                    'whope_goals',
                    'bqol_satisfaction_sum']

# Clear clipboard before run
clear_clipboard()

output_ancova_scripts(time=2, var_prefixes=vars_for_measure, covariate_time=1)
