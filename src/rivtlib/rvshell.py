import glob
import os
import shutil
import subprocess
import textwrap
from pathlib import Path


def run_shell(rshS, lD, fD, rivtD):
    uS = tS = rS = lS = ""
    blkB = False
    blkS = ""
    rsL = rshS.split("\n")
    for lS in rsL:
        lS = lS[4:]
        if lS[:10] == "_[[WRITE]]":
            blkB = True  # tag flag
            wfS = lS.split("]]")[1].strip()
            writeP = Path(fD["storeP"], "data", wfS)
            continue
        if blkB:
            if "_[[END]]" in lS:
                with open(writeP, "w") as f2:
                    f2.write(blkS)
                u1S = (
                    f"File written to: /_rvstore/data/{wfS}\n\n"
                    + textwrap.indent(blkS, "   ")
                )
                tS += (
                    f"File written to: /_rvstore/data/{wfS}\n\n"
                    + textwrap.indent(blkS, "   ")
                    + "\n\n"
                )
                rS += (
                    f"**File written to: /_rvstore/data/{wfS}**"
                    "\n\n.. code-block:: text\n\n"
                    + textwrap.indent(blkS, "   ")
                    + "\n\n"
                )

                lS = ""
                uS += u1S
                print(u1S)
                blkB = False
                blkS = ""
                continue
            blkS += lS + "\n"
            continue
        elif lS[:8] == "| COPY |":
            lcL = lS.split("|")
            fileS = lcL[4].strip()
            srcS = str(Path(fD["srcP"], "scripts", fileS))
            destS = str(Path(os.path.expandvars(lcL[3].strip())))
            sourceS = str(Path(srcS, fileS))
            for fpath in glob.glob(sourceS):
                shutil.copy(fpath, destS)
            parts = Path(srcS).parts[-4:-1]  # Take last 3 segments
            short_src = ".../" + "/".join(parts)
            parts = Path(destS).parts[-4:-1]  # Take last 3 segments
            short_dest = ".../" + "/".join(parts)
            u1S = f"Copied {fileS} from {short_src} to {short_dest}\n"
            tS += f"Copied {fileS} from {short_src} to {short_dest}\n\n"
            rS += f"**Copied {fileS} from {short_src} to {short_dest}**\n\n"
            lS += ""
            uS += u1S
            print(u1S)
            continue
        elif lS[:9] == "| SHELL |":
            lcL = lS.split("|")
            cmdS = lcL[3].strip()
            srcP = Path(fD["reptP"], "rvsrc", lcL[2].strip(), cmdS)
            cmdS = f'"{str(srcP)}"'
            try:
                result = subprocess.run(cmdS, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                print(
                    f"\033[32m------- | Command failed with exit code {e.returncode}\033[0m"
                )
            u1S = f"Run {cmdS}\n\n"
            tS += f"Run {cmdS}\n\n"
            rS += f"**Run {cmdS}**\n\n"
            lS += ""
            uS += u1S
            print(u1S)
            continue
        else:
            print(lS)
            uS += lS
            tS += lS
            rS += lS
            lS += ""

    return uS, tS, rS, lS
