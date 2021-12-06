import LibArtifact
import TablePrinter
import LogRecorder
import SimpleTranslator

def try_parse_int(v: int) -> str:
    result = 0
    try:
        result = int(v)
    except:
        return 0
    
    return result

STATUS_READY = 0
STATUS_ROLLED = 1
STATUS_UPGRADED = 2

factory = LibArtifact.ArtifactFactory()
translator = SimpleTranslator.SimpleTranslator("lang.csv", SimpleTranslator.SimpleTranslator.INDEX_CHINESE_SIMPLIFIED)
log = LogRecorder.LogRecorder(translator)
artifact_cache = []
picked_domain = None
status = STATUS_READY

while True:
    cmds = input("> ")
    cmds_sp = cmds.split(" ")

    cmd = cmds_sp[0]

    if cmd == "exit":
        break
    elif cmd == "roll":
        if status != STATUS_READY:
            log.Abort()

        artifact_cache.clear()
        if picked_domain is None:
            artifact_cache.append(factory.Generate())
        else:
            artifact_cache.append(factory.GenerateInDomain(picked_domain))
        
        TablePrinter.PrintArtifact(artifact_cache, translator)
        log.IncomeInitialArtifact(artifact_cache)

        status = STATUS_ROLLED

    elif cmd == "rolls":
        if status != STATUS_READY:
            log.Abort()

        artifact_cache.clear()
        for i in range(10):
            if picked_domain is None:
                artifact_cache.append(factory.Generate())
            else:
                artifact_cache.append(factory.GenerateInDomain(picked_domain))

        TablePrinter.PrintArtifact(artifact_cache, translator)
        log.IncomeInitialArtifact(artifact_cache)

        status = STATUS_ROLLED

    elif cmd == "up":
        if status != STATUS_ROLLED:
            print("No Artifact for Upgrading")
        else:
            for i in artifact_cache:
                i.UpgradeTo(20)
            
            TablePrinter.PrintArtifact(artifact_cache, translator)
            log.IncomeUpgradedArtifact(artifact_cache)

            status = STATUS_UPGRADED
    elif cmd == "log":
        if status != STATUS_UPGRADED:
            print("No Log for Printing")
            continue

        index = try_parse_int(cmds_sp[1])
        if index >= len(artifact_cache):
            print("Index Overflow")
            continue

        TablePrinter.PrintLog(artifact_cache[index], translator)

    elif cmd == "domain":
        TablePrinter.PrintDomain(tuple(LibArtifact.Domains.AllDomains()), translator)
    elif cmd == "pick":
        picked = int(cmds_sp[1])
        picked_domain = LibArtifact.Domains.GetDomainByIndex(picked)

# end log
if status != STATUS_READY:
    log.Abort()
log.Disposal()