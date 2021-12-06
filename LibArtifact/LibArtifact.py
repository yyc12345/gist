import random
import SimpleTranslator
from typing import Tuple

def get_random_in_list(ls):
    return ls[random.randint(0, len(ls) - 1)]

class ArtifactType:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def GetName(self, tr: SimpleTranslator.SimpleTranslator):
        return tr.Translate(self.name)

class ArtifactTypes:
    
    BloodstainedChivalry = ArtifactType(
        0, "Bloodstained Chivalry"
    )
    GladiatorsFinale = ArtifactType(
        1, "Gladiator's Finale"
    )
    WanderersTroupe = ArtifactType(
        2, "Wanderer's Troupe"
    )
    PaleFlame = ArtifactType(
        3, "Pale Flame"
    )
    ThunderingFury = ArtifactType(
        4, "Thundering Fury"
    )
    ViridescentVenerer = ArtifactType(
        5, "Viridescent Venerer"
    )
    ArchaicPetra = ArtifactType(
        6, "Archaic Petra"
    )
    CrimsonWitchOfFlames = ArtifactType(
        7, "Crimson Witch of Flames"
    )
    NoblesseOblige = ArtifactType(
        8, "Noblesse Oblige"
    )
    BlizzardStrayer = ArtifactType(
        9, "Blizzard Strayer"
    )
    HeartOfDepth = ArtifactType(
        10, "Heart of Depth"
    )
    ShimenawasReminiscence = ArtifactType(
        11, "Shimenawa's Reminiscence"
    )
    RetracingBolide = ArtifactType(
        12, "Retracing Bolide"
    )
    Thundersoother = ArtifactType(
        13, "Thundersoother"
    )
    Lavawalker = ArtifactType(
        14, "Lavawalker"
    )
    MaidenBeloved = ArtifactType(
        15, "Maiden Beloved"
    )
    TenacityOfTheMillelith = ArtifactType(
        16, "Tenacity of the Millelith"
    )
    EmblemOfSeveredFate = ArtifactType(
        17, "Emblem of Severed Fate"
    )
    HuskOfOpulentDreams = ArtifactType(
        18, "Husk of Opulent Dreams"
    )
    OceanHuedClam = ArtifactType(
        19, "Ocean-Hued Clam"
    )

class ArtifactPiece:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def GetName(self, tr: SimpleTranslator.SimpleTranslator):
        return tr.Translate(self.name)


class ArtifactPieces:
    FlowerOfLife = ArtifactPiece(0, "Flower of Life")
    PlumeOfDeath = ArtifactPiece(1, "Plume of Death")
    SandsOfEon = ArtifactPiece(2, "Sands of Eon")
    GobletOfEonothem = ArtifactPiece(3, "Goblet of Enothem")
    CircletOfLogos = ArtifactPiece(4, "Circlet of Logos")

    piecesList = (
        FlowerOfLife,
        PlumeOfDeath,
        SandsOfEon,
        GobletOfEonothem,
        CircletOfLogos
    )

    @staticmethod
    def Roll() -> ArtifactPiece:
        return get_random_in_list(ArtifactPieces.piecesList)

    
class MainStatType:
    HP = (717, 920, 1123, 1326, 1530, 1733, 1936, 2139, 2342, 2545, 2749, 2952, 3155, 3358, 3561, 3764, 3967, 4171, 4374, 4577, 4780)
    ATK = (47, 60, 73, 86, 100, 113, 126, 139, 152, 166, 179, 192, 205, 219, 232, 245, 258, 272, 285, 298, 311)
    DEFPercent = (7, 9, 11, 12.90, 14.90, 16.90, 18.90, 20.90, 22.80, 24.80, 26.80, 28.80, 30.80, 32.80, 34.70, 36.70, 38.70, 40.70, 42.70, 44.60, 46.60)
    HPPercent = (8.70, 11.20, 13.70, 16.20, 18.60, 21.10, 23.60, 26.10, 28.60, 31, 33.50, 36, 38.50, 40.90, 43.40, 45.90, 48.40, 50.80, 53.30, 55.80, 58.30)
    ATKPercent = (7, 9, 11, 12.90, 14.90, 16.90, 18.90, 20.90, 22.80, 24.80, 26.80, 28.80, 30.80, 32.80, 34.70, 36.70, 38.70, 40.70, 42.70, 44.60, 46.60)
    ElementalMastery = (28, 36, 44, 52, 60, 68, 76, 84, 91, 99, 107, 115, 123, 131, 139, 147, 155, 163, 171, 179, 187)
    EnergyRecharge = (7.80, 10, 12.20, 14.40, 16.60, 18.80, 21, 23.20, 25.40, 27.60, 29.80, 32, 34.20, 36.40, 38.60, 40.80, 43, 45.20, 47.40, 49.60, 51.80)
    PhysicalDMGBonus = (8.70, 11.20, 13.70, 16.20, 18.60, 21.10, 23.60, 26.10, 28.60, 31, 33.50, 36, 38.50, 40.90, 43.40, 45.90, 48.40, 50.80, 53.30, 55.80, 58.30)
    ElementDMGBonus = (7, 9, 11, 12.90, 14.90, 16.90, 18.90, 20.90, 22.80, 24.80, 26.80, 28.80, 30.80, 32.80, 34.70, 36.70, 38.70, 40.70, 42.70, 44.60, 46.60)
    CRITRate = (4.70, 6, 7.30, 8.60, 9.90, 11.30, 12.60, 13.90, 15.20, 16.60, 17.90, 19.20, 20.50, 21.80, 23.20, 24.50, 25.80, 27.10, 28.40, 29.80, 31.10)
    CRITDMG = (9.30, 12, 14.60, 17.30, 19.90, 22.50, 25.20, 27.80, 30.50, 33.10, 35.70, 38.40, 41, 43.70, 46.30, 49, 51.60, 54.20, 56.90, 59.50, 62.20)
    HealingBonus = (5.40, 6.90, 8.40, 10, 11.50, 13, 14.50, 16.10, 17.60, 19.10, 20.60, 22.10, 23.70, 25.20, 26.70, 28.20, 29.80, 31.30, 32.80, 34.30, 35.90)

    def __init__(self, id: int, name: str, is_percent: bool, roll: Tuple[float]):
        self.id = id
        self.name = name
        self.is_percent = is_percent
        self.roll = roll

    def GetName(self, tr: SimpleTranslator.SimpleTranslator):
        return tr.Translate(self.name)

    def ProcessNumber(self, num: float) -> str:
        if self.is_percent:
            return "{:.1f}%".format(num)
        else:
            return str(int(round(num)))

    def GetNumber(self, level: int) -> float:
        if (level < 0 or level > 20):
            raise Exception("cao ni ma")
        return self.roll[level]

class SubstatType:
    HP = (209, 239, 269, 299)
    DEF = (16, 19, 21, 23)
    ATK = (14, 16, 18, 19)
    HPPercent = (4.10, 4.70, 5.30, 5.80)
    DEFPercent = (5.10, 5.80, 6.60, 7.30)
    ATKPercent = (4.10, 4.70, 5.30, 5.80)
    ElementalMastery = (16, 19, 21, 23)
    EnergyRecharge = (4.50, 5.20, 5.80, 6.50)
    CRITRate = (2.70, 3.10, 3.50, 3.90)
    CRITDMG = (5.40, 6.20, 7, 7.80)

    def __init__(self, id: int, name: str, is_percent: bool, roll: Tuple[float], matched_main_stat: MainStatType):
        self.id = id
        self.name = name
        self.is_percent = is_percent
        self.roll = roll
        self.matched_main_stat = matched_main_stat

    def GetName(self, tr: SimpleTranslator.SimpleTranslator):
        return tr.Translate(self.name)

    def IsConflict(self, main: MainStatType) -> bool:
        if self.matched_main_stat is None:
            return False

        return main.id == self.matched_main_stat.id

    def ProcessNumber(self, num: float) -> str:
        if self.is_percent:
            return "{:.1f}%".format(num)
        else:
            return str(int(round(num)))

    def Roll(self) -> float:
        return self.roll[random.randint(0, 3)]

class MainStatTypes:
    HP = MainStatType(0, "HP", False, MainStatType.HP)
    ATK = MainStatType(1, "ATK", False, MainStatType.ATK)
    DEFPercent = MainStatType(2, "DEF", True, MainStatType.DEFPercent)
    HPPercent = MainStatType(3, "HP", True, MainStatType.HPPercent)
    ATKPercent = MainStatType(4, "ATK", True, MainStatType.ATKPercent)
    ElementalMastery = MainStatType(5, "Elemental Mastery", False, MainStatType.ElementalMastery)
    EnergyRecharge = MainStatType(6, "Energy Recharge", True, MainStatType.EnergyRecharge)
    PhysicalDMGBonus = MainStatType(7, "Physical DMG Bonus", True, MainStatType.PhysicalDMGBonus)

    AnemoDMGBonus = MainStatType(8, "Anemo DMG Bonus", True, MainStatType.ElementDMGBonus)
    CryoDMGBonus = MainStatType(9, "Cryo DMG Bonus", True, MainStatType.ElementDMGBonus)
    DendroDMGBonus = MainStatType(10, "Dendro DMG Bonus", True, MainStatType.ElementDMGBonus)
    ElectroDMGBonus = MainStatType(11, "Electro DMG Bonus", True, MainStatType.ElementDMGBonus)
    GeoDMGBonus = MainStatType(12, "Geo DMG Bonus", True, MainStatType.ElementDMGBonus)
    HydroDMGBonus = MainStatType(13, "Hydro DMG Bonus", True, MainStatType.ElementDMGBonus)
    PyroDMGBonus = MainStatType(14, "Pyro DMG Bonus", True, MainStatType.ElementDMGBonus)

    CRITRate = MainStatType(15, "CRIT Rate", True, MainStatType.CRITRate)
    CRITDMG = MainStatType(16, "CRIT DMG", True, MainStatType.CRITDMG)
    HealingBonus = MainStatType(17, "Healing Bonus", True, MainStatType.HealingBonus)

    sands_MainStatList = (
        HPPercent,
        DEFPercent,
        ATKPercent,
        EnergyRecharge,
        ElementalMastery
    )
    goblet_MainStatList = (
        HPPercent,
        DEFPercent,
        ATKPercent,
        PhysicalDMGBonus,
        AnemoDMGBonus,
        CryoDMGBonus,
        DendroDMGBonus,
        ElectroDMGBonus,
        GeoDMGBonus,
        HydroDMGBonus,
        PyroDMGBonus,
        ElementalMastery
    )
    circlet_MainStatList = (
        HPPercent,
        DEFPercent,
        ATKPercent,
        ElementalMastery,
        CRITRate,
        CRITDMG,
        HealingBonus
    )

    @staticmethod
    def Roll(piece: ArtifactPiece) -> MainStatType:
        if (piece.id == ArtifactPieces.FlowerOfLife.id):
            return MainStatTypes.HP
        elif (piece.id == ArtifactPieces.PlumeOfDeath.id):
            return MainStatTypes.ATK
        elif (piece.id == ArtifactPieces.SandsOfEon.id):
            return get_random_in_list(MainStatTypes.sands_MainStatList)
        elif (piece.id == ArtifactPieces.GobletOfEonothem.id):
            return get_random_in_list(MainStatTypes.goblet_MainStatList)
        elif (piece.id == ArtifactPieces.CircletOfLogos.id):
            return get_random_in_list(MainStatTypes.circlet_MainStatList)
        else:
            raise Exception("cao ni ma")

class SubstatTypes:
    HP = SubstatType(0, "HP", False, SubstatType.HP, MainStatTypes.HP)
    DEF = SubstatType(1, "DEF", False, SubstatType.DEF, None)
    ATK = SubstatType(2, "ATK", False, SubstatType.ATK, MainStatTypes.ATK)
    HPPercent = SubstatType(3, "HP", True, SubstatType.HPPercent, MainStatTypes.HPPercent)
    DEFPercent = SubstatType(4, "DEF", True, SubstatType.DEFPercent, MainStatTypes.DEFPercent)
    ATKPercent = SubstatType(5, "ATK", True, SubstatType.ATKPercent, MainStatTypes.ATKPercent)
    ElementalMastery =SubstatType(6, "Elemental Mastery", False, SubstatType.ElementalMastery, MainStatTypes.ElementalMastery)
    EnergyRecharge = SubstatType(7, "Energy Recharge", True, SubstatType.EnergyRecharge, MainStatTypes.EnergyRecharge)
    CRITRate = SubstatType(8, "CRIT Rate", True, SubstatType.CRITRate, MainStatTypes.CRITRate)
    CRITDMG = SubstatType(9, "CRIT DMG", True, SubstatType.CRITDMG, MainStatTypes.CRITDMG)

    allStats = (
        HP,
        DEF,
        ATK,
        HPPercent,
        DEFPercent,
        ATKPercent,
        ElementalMastery,
        EnergyRecharge,
        CRITRate,
        CRITDMG
    )

    @staticmethod
    def Roll(main_stat: MainStatType) -> Tuple[SubstatType]:
        ls = []
        for i in SubstatTypes.allStats:
            if not i.IsConflict(main_stat):
                ls.append(i)

        random.shuffle(ls)
        return tuple(ls[:4])


class Artifact:

    upgradeHelper = (0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5)

    def __init__(self, artifact_type: ArtifactType, artifact_piece: ArtifactPiece):
        self.upgrade_log = []
        self.level = 0

        self.artifact_type = artifact_type
        self.artifact_piece = artifact_piece

        # gen type
        self.main_stat = MainStatTypes.Roll(self.artifact_piece)
        self.substat = SubstatTypes.Roll(self.main_stat)

        # gen data
        self.substat_data = [0, 0, 0, 0]
        self.__upgrade_substat(0, False)
        self.__upgrade_substat(1, False)
        self.__upgrade_substat(2, False)
        if (random.randint(0, 3) == 0):
            self.__upgrade_substat(3, False)   # 4th substat have 1 in 4 chance with initial value

    def UpgradeTo(self, new_level: int):
        if (new_level < self.level or new_level > 20):
            raise Exception("cao ni ma")

        for i in range(Artifact.upgradeHelper[new_level] - Artifact.upgradeHelper[self.level]):
            index = random.randint(0, 3)
            if self.substat_data[3] == 0:
                index = 3
            self.__upgrade_substat(index, True)

        self.level = new_level

    def GetArtifactTypeName(self, tr: SimpleTranslator.SimpleTranslator):
        return self.artifact_type.GetName(tr)

    def GetArtifactPieceName(self, tr: SimpleTranslator.SimpleTranslator):
        return self.artifact_piece.GetName(tr)

    def GetMainStatName(self, tr: SimpleTranslator.SimpleTranslator):
        return self.main_stat.GetName(tr)

    def GetMainStatData(self):
        return self.main_stat.ProcessNumber(self.main_stat.GetNumber(self.level))

    def GetSubStatName(self, index, tr: SimpleTranslator.SimpleTranslator):
        self.__check_substat_index(index)
        return self.substat[index].GetName(tr)

    def GetSubStatData(self, index):
        self.__check_substat_index(index)
        return self.substat[index].ProcessNumber(self.substat_data[index])

    def ShouldShowSubstat(self, index):
        self.__check_substat_index(index)
        return self.substat_data[index] != 0

    def GetUpgradeLog(self):
        for i in self.upgrade_log:
            yield i

    def __check_substat_index(self, index):
        if (index < 0 or index >= 4):
            raise Exception("cao ni ma")

    def __upgrade_substat(self, index: int, send_to_log: bool):
        num = self.substat[index].Roll()
        self.substat_data[index] += num

        if send_to_log:
            self.upgrade_log.append((index, self.substat[index].ProcessNumber(num)))

class Domain:
    def __init__(self, id: int, name: str, artifact_list: Tuple[ArtifactType]):
        self.id = id
        self.name = name
        self.artifact_list = artifact_list

    def GetName(self, tr: SimpleTranslator.SimpleTranslator):
        return tr.Translate(self.name)

    def Roll(self) -> ArtifactType:
        return get_random_in_list(self.artifact_list)

class Domains:
    MidsummerCourtyard = Domain(0, "Midsummer Courtyard", (ArtifactTypes.ThunderingFury, ArtifactTypes.Thundersoother))
    ValleyOfRemembrance = Domain(1, "Valley of Remembrance", (ArtifactTypes.ViridescentVenerer, ArtifactTypes.MaidenBeloved))
    DomainOfGuyun = Domain(2, "Domain of Guyun", (ArtifactTypes.ArchaicPetra, ArtifactTypes.RetracingBolide))
    HiddenPalaceOfZhouFormula = Domain(3, "Hidden Palace of Zhou Formula", (ArtifactTypes.CrimsonWitchOfFlames, ArtifactTypes.Lavawalker))
    ClearPoolAndMountainCavern = Domain(4, "Clear Pool and Mountain Cavern", (ArtifactTypes.BloodstainedChivalry, ArtifactTypes.NoblesseOblige))
    PeakOfVindagnyr = Domain(5, "Peak of Vindagnyr", (ArtifactTypes.BlizzardStrayer, ArtifactTypes.HeartOfDepth))
    RidgeWatch = Domain(6, "Ridge Watch", (ArtifactTypes.TenacityOfTheMillelith, ArtifactTypes.PaleFlame))
    MomijiDyedCourt = Domain(7, "Momiji-Dyed Court", (ArtifactTypes.ShimenawasReminiscence, ArtifactTypes.EmblemOfSeveredFate))
    SlumberingCourt = Domain(8, "Slumbering Court", (ArtifactTypes.HuskOfOpulentDreams, ArtifactTypes.OceanHuedClam))

    allDomains = (
        MidsummerCourtyard,
        ValleyOfRemembrance,
        DomainOfGuyun,
        HiddenPalaceOfZhouFormula,
        ClearPoolAndMountainCavern,
        PeakOfVindagnyr,
        RidgeWatch,
        MomijiDyedCourt,
        SlumberingCourt
    )

    @staticmethod
    def Roll() -> Domain:
        return get_random_in_list(Domains.allDomains)

    def GetDomainByIndex(index: int):
        return Domains.allDomains[index]

    def AllDomains():
        for i in Domains.allDomains:
            yield i

class ArtifactFactory:

    @staticmethod
    def Generate() -> Artifact:
        return Artifact(
            Domains.Roll().Roll(),
            ArtifactPieces.Roll()
        )

    @staticmethod
    def GenerateInDomain(domain: Domain) -> Artifact:
        return Artifact(
            domain.Roll(),
            ArtifactPieces.Roll()
        )
