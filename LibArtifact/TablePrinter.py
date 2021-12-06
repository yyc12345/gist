import LibArtifact
import tabulate
import SimpleTranslator
from typing import Tuple, List

artifact_headers = [
    "Type",
    "Piece",
    "Main Stat",
    "",
    "Substat 1",
    "",
    "Substat 2",
    "",
    "Substat 3",
    "",
    "Substat 4",
    ""
]

log_headers = [
    "Substat",
    ""
]

domain_headers = [
    "Index",
    "Name",
    "Artifact"
]

def PrintArtifact(ls: List[LibArtifact.Artifact], tr: SimpleTranslator.SimpleTranslator):
    table = []

    for artifact in ls:
        row = [
            artifact.GetArtifactTypeName(tr),
            artifact.GetArtifactPieceName(tr),
            artifact.GetMainStatName(tr),
            artifact.GetMainStatData()
        ]
        for i in range(4):
            if not artifact.ShouldShowSubstat(i):
                row.append("-")
                row.append("-")
            else:
                row.append(artifact.GetSubStatName(i, tr))
                row.append(artifact.GetSubStatData(i))

        table.append(row)

    print(tabulate.tabulate(table, headers = artifact_headers, tablefmt="grid"))
            
def PrintLog(artifact: LibArtifact.Artifact, tr: SimpleTranslator.SimpleTranslator):
    table = []

    for i in artifact.GetUpgradeLog():
        row = [
            artifact.GetSubStatName(i[0], tr),
            i[1]
        ]
        table.append(row)

    print(tabulate.tabulate(table, headers = log_headers, tablefmt="pretty"))

def PrintDomain(ls: Tuple[LibArtifact.Domain], tr: SimpleTranslator.SimpleTranslator):
    table = []

    for i in ls:
        table.append([
            i.id,
            i.GetName(tr),
            ', '.join(map(lambda x: x.GetName(tr), i.artifact_list))
        ])

    print(tabulate.tabulate(table, headers = domain_headers, tablefmt="grid"))