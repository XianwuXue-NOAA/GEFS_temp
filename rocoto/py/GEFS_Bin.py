import GEFS_XML_For_Tasks as gefs_xml_for_tasks


# ===========================================================
def create_bin_file(dicBase):
    '''
        Create crontab to execute rocotorun every cronint (5) minutes
    '''
    ##########################################################
    # Generate crotab file based on different computers.
    #
    # Inputs (via environment variables):
    #         dicBase         : The base configuration from user config file
    #
    # Outputs:
    #         modify bin files and write back to the corresponsding
    #
    #
    ##########################################################

    taskname = 'forecast_high'  # 06
    if DoesTaskExist(dicBase, taskname):
        rw_bin_forecast_high(taskname, dicBase)

    taskname = 'forecast_low'
    if DoesTaskExist(dicBase, taskname):
        rw_bin_forecast_high(taskname, dicBase)

    taskname = 'prdgen_high'
    if DoesTaskExist(dicBase, taskname):
        rw_bin_prdgen(taskname, dicBase)

    taskname = 'prdgen_low'
    if DoesTaskExist(dicBase, taskname):
        rw_bin_prdgen(taskname, dicBase)

    taskname = 'prdgen_gfs'
    if DoesTaskExist(dicBase, taskname):
        if not DoesTaskExist(dicBase, 'prdgen_high'):
            rw_bin_prdgen(taskname, dicBase)

    taskname = 'ensstat_high'
    if DoesTaskExist(dicBase, taskname):
        rw_bin_ensstat(taskname, dicBase)

    taskname = 'ensstat_low'
    if DoesTaskExist(dicBase, taskname):
        rw_bin_ensstat(taskname, dicBase)

    taskname = 'gempak'
    if DoesTaskExist(dicBase, taskname):
        rw_bin_gempak(taskname, dicBase)

    taskname = 'avgspr_gempak'
    if DoesTaskExist(dicBase, taskname):
        rw_bin_avgspr_gempak(taskname, dicBase)


# ===========================================================
def rw_bin_avgspr_gempak(taskname, dicBase):
    import sys
    import os

    sSep = "/"
    if sys.platform == 'win32':
        sSep = r'\\'

    sPath = dicBase["GEFS_ROCOTO"]

    sPath += sSep + "bin" + sSep + dicBase["WHERE_AM_I"] + sSep
    sInput_File = sPath + "{0}.sh".format(taskname)

    if not os.path.exists(sInput_File):
        print("Please check whether you have the input file: " + sInput_File)
        return

    if "PRDGEN_STREAMS" not in dicBase:
        print("Please check whether you have the 'PRDGEN_STREAMS' variable in your user_full.conf and gefs_dev.parm")
        return

    Total_tasks = 2
    nGEMPAK_RES = 1
    if "GEMPAK_RES" in dicBase:
        nGEMPAK_RES = len(dicBase["GEMPAK_RES"].split())
        Total_tasks *= nGEMPAK_RES

    WHERE_AM_I = dicBase['WHERE_AM_I'].lower()

    iPPN = Total_tasks
    iNodes = 1

    sLines = ""
    with open(sInput_File, "r") as f:
        for sLine in f:
            # print(sLine)
            sLine1 = sLine.strip()

            if WHERE_AM_I == "cray":
                if sLine1.startswith("export total_tasks="):
                    sLine = 'export total_tasks={0}\n'.format(Total_tasks)
                if sLine1.startswith("export taskspernode="):
                    sLine = 'export taskspernode={0}\n'.format(iPPN)

            elif WHERE_AM_I == "theia":
                pass

            elif WHERE_AM_I == "wcoss_dell_p3":
                if sLine1.startswith("export total_tasks="):
                    sLine = 'export total_tasks={0}\n'.format(Total_tasks)
                if sLine1.startswith("export taskspernode="):
                    sLine = 'export taskspernode={0}\n'.format(iPPN)

            elif WHERE_AM_I == "wcoss_ibm":
                if sLine1.startswith("export total_tasks="):
                    sLine = 'export total_tasks={0}\n'.format(Total_tasks)
                if sLine1.startswith("export taskspernode="):
                    sLine = 'export taskspernode={0}\n'.format(iPPN)

            sLines += sLine
            # fh.write(sLine)

    fh = open(sInput_File, 'w')
    fh.writelines(sLines)
    fh.flush()
    fh.close()


# ===========================================================
def rw_bin_gempak(taskname, dicBase):
    import sys
    import os

    sSep = "/"
    if sys.platform == 'win32':
        sSep = r'\\'

    sPath = dicBase["GEFS_ROCOTO"]

    sPath += sSep + "bin" + sSep + dicBase["WHERE_AM_I"] + sSep
    sInput_File = sPath + "{0}.sh".format(taskname)

    if not os.path.exists(sInput_File):
        print("Please check whether you have the input file: " + sInput_File)
        return

    if "PRDGEN_STREAMS" not in dicBase:
        print("Please check whether you have the 'PRDGEN_STREAMS' variable in your user_full.conf and gefs_dev.parm")
        return

    ncores_per_node = gefs_xml_for_tasks.Get_NCORES_PER_NODE(dicBase)
    npert = int(dicBase["NPERT"])
    Total_tasks = npert + 1
    nGEMPAK_RES = 1
    if "GEMPAK_RES" in dicBase:
        nGEMPAK_RES = len(dicBase["GEMPAK_RES"].split())
        Total_tasks *= nGEMPAK_RES

    WHERE_AM_I = dicBase['WHERE_AM_I'].lower()

    if (npert + 1) <= ncores_per_node:
        iNodes = nGEMPAK_RES
        iPPN = (npert + 1)
    else:
        if npert == 30 and WHERE_AM_I.upper() == "THEIA":
            iPPN = 3
            iNodes = 31
        else:
            iPPN = ncores_per_node
            iNodes = int(Total_tasks / (iPPN * 1.0) + 0.5)

    sLines = ""
    with open(sInput_File, "r") as f:
        for sLine in f:
            # print(sLine)
            sLine1 = sLine.strip()

            if WHERE_AM_I == "cray":
                if sLine1.startswith("export total_tasks="):
                    sLine = 'export total_tasks={0}\n'.format(Total_tasks)
                if sLine1.startswith("export taskspernode="):
                    sLine = 'export taskspernode={0}\n'.format(iPPN)

            elif WHERE_AM_I == "theia":
                pass

            elif WHERE_AM_I == "wcoss_dell_p3":
                if sLine1.startswith("export total_tasks="):
                    sLine = 'export total_tasks={0}\n'.format(Total_tasks)
                if sLine1.startswith("export taskspernode="):
                    sLine = 'export taskspernode={0}\n'.format(iPPN)

            elif WHERE_AM_I == "wcoss_ibm":
                if sLine1.startswith("export total_tasks="):
                    sLine = 'export total_tasks={0}\n'.format(Total_tasks)
                if sLine1.startswith("export taskspernode="):
                    sLine = 'export taskspernode={0}\n'.format(iPPN)

            sLines += sLine
            # fh.write(sLine)

    fh = open(sInput_File, 'w')
    fh.writelines(sLines)
    fh.flush()
    fh.close()


# ===========================================================
def rw_bin_ensstat(taskname, dicBase):
    import sys
    import os

    sSep = "/"
    if sys.platform == 'win32':
        sSep = r'\\'

    sPath = dicBase["GEFS_ROCOTO"]

    sPath += sSep + "bin" + sSep + dicBase["WHERE_AM_I"] + sSep
    sInput_File = sPath + "{0}.sh".format(taskname)

    if not os.path.exists(sInput_File):
        print("Please check whether you have the input file: " + sInput_File)
        return

    if "PRDGEN_STREAMS" not in dicBase:
        print("Please check whether you have the 'PRDGEN_STREAMS' variable in your user_full.conf and gefs_dev.parm")
        return

    iTotal_Tasks = len(dicBase["PRDGEN_STREAMS"].split())
    WHERE_AM_I = dicBase['WHERE_AM_I'].lower()
    sLines = ""
    with open(sInput_File, "r") as f:
        for sLine in f:
            # print(sLine)
            sLine1 = sLine.strip()

            if WHERE_AM_I == "cray":
                if sLine1.startswith("export total_tasks="):
                    sLine = 'export total_tasks={0}\n'.format(iTotal_Tasks)

            elif WHERE_AM_I == "theia":
                pass

            elif WHERE_AM_I == "wcoss_dell_p3":
                if sLine1.startswith("export total_tasks="):
                    sLine = 'export total_tasks={0}\n'.format(iTotal_Tasks)

            elif WHERE_AM_I == "wcoss_ibm":
                if sLine1.startswith("export total_tasks="):
                    sLine = 'export total_tasks={0}\n'.format(iTotal_Tasks)

            sLines += sLine
            # fh.write(sLine)

    fh = open(sInput_File, 'w')
    fh.writelines(sLines)
    fh.flush()
    fh.close()


# ===========================================================
def rw_bin_prdgen(taskname, dicBase):
    import sys
    import os

    sSep = "/"
    if sys.platform == 'win32':
        sSep = r'\\'

    sPath = dicBase["GEFS_ROCOTO"]

    sPath += sSep + "bin" + sSep + dicBase["WHERE_AM_I"] + sSep
    if taskname != "prdgen_gfs":
        sInput_File = sPath + taskname + ".sh"
    else:
        sInput_File = sPath + "prdgen_high.sh"

    if not os.path.exists(sInput_File):
        print("Please check whether you have the input file: " + sInput_File)
        return

    if "PRDGEN_STREAMS" not in dicBase:
        print("Please check whether you have the 'PRDGEN_STREAMS' variable in your user_full.conf and gefs_dev.parm")
        return

    iTotal_Tasks = len(dicBase["PRDGEN_STREAMS"].split())
    WHERE_AM_I = dicBase['WHERE_AM_I'].lower()
    sLines = ""
    with open(sInput_File, "r") as f:
        for sLine in f:
            # print(sLine)
            sLine1 = sLine.strip()

            if WHERE_AM_I == "cray":
                if sLine1.startswith("export total_tasks="):
                    sLine = 'export total_tasks={0}\n'.format(iTotal_Tasks)

            elif WHERE_AM_I == "theia":
                pass

            elif WHERE_AM_I == "wcoss_dell_p3":
                if sLine1.startswith("export total_tasks="):
                    sLine = 'export total_tasks={0}\n'.format(iTotal_Tasks)

            elif WHERE_AM_I == "wcoss_ibm":
                if sLine1.startswith("export total_tasks="):
                    sLine = 'export total_tasks={0}\n'.format(iTotal_Tasks)

            sLines += sLine
            # fh.write(sLine)

    fh = open(sInput_File, 'w')
    fh.writelines(sLines)
    fh.flush()
    fh.close()


# ===========================================================
def rw_bin_forecast_high(taskname, dicBase):
    import sys
    import os

    sSep = "/"
    if sys.platform == 'win32':
        sSep = r'\\'

    sPath = dicBase["GEFS_ROCOTO"]

    sPath += sSep + "bin" + sSep + dicBase["WHERE_AM_I"] + sSep
    sInput_File = sPath + taskname + ".sh"

    if not os.path.exists(sInput_File):
        print("Please check whether you have the input file: " + sInput_File)
        return

    WHERE_AM_I = dicBase['WHERE_AM_I']

    iTotal_Tasks, iNodes, iPPN, iTPP = gefs_xml_for_tasks.calc_fcst_resources(dicBase)

    # sNodes = "{0}:ppn={1}:tpp={2}".format(iNodes, iPPN, iTPP)

    sLines = ""
    with open(sInput_File, "r") as f:
        for sLine in f:
            # print(sLine)
            sLine1 = sLine.strip()

            if WHERE_AM_I == "cray":
                if sLine1.startswith("export gefsmpexec="):
                    sLine = 'export gefsmpexec=" aprun -b -j1 -n{0} -N{1} -d{2} -cc depth "\n'.format(iTotal_Tasks, iPPN, iTPP)

            elif WHERE_AM_I == "theia":
                if sLine1.startswith("export total_tasks="):
                    sLine = 'export total_tasks={0}\n'.format(iTotal_Tasks)

                if sLine1.startswith("export OMP_NUM_THREADS="):
                    sLine = 'export OMP_NUM_THREADS={0}\n'.format(iTPP)

                if sLine1.startswith("export taskspernode"):
                    sLine = 'export taskspernode={0}\n'.format(iPPN)

            elif WHERE_AM_I == "wcoss_dell_p3":
                if sLine1.startswith("export gefsmpexec="):
                    sLine = 'export gefsmpexec=" mpirun -n {0} "\n'.format(iTotal_Tasks)

            sLines += sLine
            # fh.write(sLine)

    fh = open(sInput_File, 'w')
    fh.writelines(sLines)
    fh.flush()
    fh.close()


# =========================================================
def DoesTaskExist(dicBase, taskname):
    taskname_num = int(dicBase['taskname_num'.upper()])

    if taskname_num <= 0:
        return False

    for k in range(taskname_num):
        sTaskName = dicBase["taskname_{0}".format(k + 1).upper()]
        if sTaskName == taskname:
            return True

    return False


# ===========================================================
def main():
    # for test this function

    g_OnlyForTest = True
    g_Rocoto_ForTest = ""

    import GEFS_Crontab as gefs_crontab
    import GEFS_Parm as gefs_parm
    import GEFS_UserConfig as gefs_config

    import GEFS_XML as gefs_xml
    import GEFS_XML_For_Tasks as gefs_xml_for_tasks

    import os, sys
    sSep = "/"
    if sys.platform == 'win32':
        sSep = r'\\'

    print("--Starting to generate all files you need!")

    print("--Getting user config file!")
    sConfig, sRocoto_WS = gefs_config.get_config_file(OnlyForTest=g_OnlyForTest)

    g_Rocoto_ForTest = sRocoto_WS

    print("--Reading user config file...")

    dicBase = gefs_config.read_config(sConfig)

    print("--Checking the must parameters for the config file")
    sMust_Items = ['SDATE', 'EDATE']  # , 'First'.upper(), 'Last'.upper()]
    for sMust_Item in sMust_Items:
        if sMust_Item not in dicBase:
            print("You need assign value of {0}".format(sMust_Item))
            exit(-1)

    # Get the default value
    print("--Getting default values from default user config file!")
    gefs_config.get_and_merge_default_config(dicBase)

    # Only for test
    if g_OnlyForTest:
        dicBase["GEFS_ROCOTO"] = g_Rocoto_ForTest
        dicBase["WORKDIR"] = g_Rocoto_ForTest

    print("--Assign default values for the config file")
    gefs_xml.assign_default_for_xml_def(dicBase, sRocoto_WS=sRocoto_WS)

    print(dicBase["WHERE_AM_I"])

    create_bin_file(dicBase)


# ===========================================================
if __name__ == '__main__':
    import sys

    main()

    print("--Done to generate all files!")
    sys.exit(0)
