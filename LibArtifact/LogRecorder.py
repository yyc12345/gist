import LibArtifact
import time
import SimpleTranslator
from typing import Tuple, List

class LogRecorder:

    default_header1 = ",,-,Initial,,,,,,,,,,-,Upgraded,,,,,,,,,,-,Log,,,,,,,,,\n"
    default_header2 = "Type,Piece,-,Main Stat,,Substat 1,,Substat 2,,Substat 3,,Substat 4,,-,Main Stat,,Substat 1,,Substat 2,,Substat 3,,Substat 4,,-,Log 1,,Log 2,,Log 3,,Log 4,,Log 5,\n"

    blank_part2 = ",-,,,,,,,,,,,-,,,,,,,,,,"

    STATUS_READY = 0
    STATUS_INITIAL = 1
    STATUS_UPGRADED = 2

    def __init__(self, tr: SimpleTranslator.SimpleTranslator):
        self.fs = open(self.__generate_filename(), "w")
        self.fs.write(LogRecorder.default_header1)
        self.fs.write(LogRecorder.default_header2)
        self.pending_data = []
        self.tr = tr
        self.status = LogRecorder.STATUS_READY

    def IncomeInitialArtifact(self, ls: List[LibArtifact.Artifact]):
        if len(self.pending_data) != 0 or self.status != LogRecorder.STATUS_READY:
            raise Exception("cao ni ma")

        for artifact in ls:
            self.pending_data.append("{},{},-,{}".format(
                artifact.GetArtifactTypeName(self.tr),
                artifact.GetArtifactPieceName(self.tr),
                self.__gennerate_artifact_info(artifact)
            ))

        self.status = LogRecorder.STATUS_INITIAL

    def IncomeUpgradedArtifact(self, ls: List[LibArtifact.Artifact]):
        if len(self.pending_data) != len(ls) or self.status != LogRecorder.STATUS_INITIAL:
            raise Exception("cao ni ma")

        for index, artifact in enumerate(ls):
            self.pending_data[index] += ",-,{},-,{}".format(
                self.__gennerate_artifact_info(artifact),
                self.__generate_artifact_log(artifact)
            )

        self.status = LogRecorder.STATUS_UPGRADED

    def Abort(self):
        if self.status == LogRecorder.STATUS_INITIAL:
            for i in self.pending_data:
                self.fs.write(i)
                self.fs.write(LogRecorder.blank_part2)
                self.fs.write("\n")
        elif self.status == LogRecorder.STATUS_UPGRADED:
            for i in self.pending_data:
                self.fs.write(i)
                self.fs.write("\n")
        else:
            raise Exception("cao ni ma")

        self.pending_data.clear()
        self.status = LogRecorder.STATUS_READY

    def Disposal(self):
        self.fs.close()

    def __gennerate_artifact_info(self, artifact: LibArtifact.Artifact):
        row = [
            artifact.GetMainStatName(self.tr),
            artifact.GetMainStatData()
        ]

        for i in range(4):
            if not artifact.ShouldShowSubstat(i):
                row.append("-")
                row.append("-")
            else:
                row.append(artifact.GetSubStatName(i, self.tr))
                row.append(artifact.GetSubStatData(i))

        return ','.join(row)

    def __generate_artifact_log(self, artifact: LibArtifact.Artifact):
        row = []
        counter = 0

        for i in artifact.GetUpgradeLog():
            row.append(artifact.GetSubStatName(i[0], self.tr))
            row.append(i[1])
            counter += 1

        while True:
            if counter == 5:
                break

            row.append("")
            row.append("")

            counter += 1

        return ','.join(row)

    def __generate_filename(self):
        return time.strftime("%Y%m%d%H%M%S.csv", time.localtime())
