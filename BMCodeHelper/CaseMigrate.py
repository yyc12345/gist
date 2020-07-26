fr=open('migrating.txt', 'r')

caseDict = {}
oldList = [
    "Ball_LightningSphere1.bmp",
    "Ball_LightningSphere2.bmp",
    "Ball_LightningSphere3.bmp",
    "Ball_Paper.bmp",
    "Ball_Stone.bmp",
    "Ball_Wood.bmp",
    "Brick.bmp",
    "Button01_deselect.tga",
    "Button01_select.tga",
    "Button01_special.tga",
    "Column_beige.bmp",
    "Column_beige_fade.tga",
    "Column_blue.bmp",
    "Dome.bmp",
    "DomeEnvironment.bmp",
    "DomeShadow.tga",
    "ExtraBall.bmp",
    "ExtraParticle.bmp",
    "E_Holzbeschlag.bmp",
    "FloorGlow.bmp",
    "Floor_Side.bmp",
    "Floor_Top_Border.bmp",
    "Floor_Top_Borderless.bmp",
    "Floor_Top_Checkpoint.bmp",
    "Floor_Top_Flat.bmp",
    "Floor_Top_Profil.bmp",
    "Floor_Top_ProfilFlat.bmp",
    "Font_1.tga",
    "Gravitylogo_intro.bmp",
    "HardShadow.bmp",
    "Laterne_Glas.bmp",
    "Laterne_Schatten.tga",
    "Laterne_Verlauf.tga",
    "Metal_stained.bmp",
    "Misc_Ufo.bmp",
    "Misc_UFO_Flash.bmp",
    "Modul03_Floor.bmp",
    "Modul03_Wall.bmp",
    "Modul11_13_Wood.bmp",
    "Modul11_Wood.bmp",
    "Modul15.bmp",
    "Modul16.bmp",
    "Modul18.bmp",
    "Modul18_Gitter.tga",
    "Modul30_d_Seiten.bmp",
    "Particle_Flames.bmp",
    "Particle_Smoke.bmp",
    "PE_Bal_balloons.bmp",
    "PE_Bal_platform.bmp",
    "PE_Ufo_env.bmp",
    "P_Extra_Life_Oil.bmp",
    "P_Extra_Life_Particle.bmp",
    "P_Extra_Life_Shadow.bmp",
    "Rail_Environment.bmp",
    "sandsack.bmp",
    "SkyLayer.bmp",
    "Sky_Vortex.bmp",
    "Stick_Bottom.tga",
    "Stick_Stripes.bmp",
    "Target.bmp",
    "Tower_Roof.bmp",
    "Trafo_Environment.bmp",
    "Trafo_FlashField.bmp",
    "Trafo_Shadow_Big.tga",
    "Wood_Metal.bmp",
    "Wood_MetalStripes.bmp",
    "Wood_Misc.bmp",
    "Wood_Nailed.bmp",
    "Wood_Old.bmp",
    "Wood_Panel.bmp",
    "Wood_Plain.bmp",
    "Wood_Plain2.bmp",
    "Wood_Raft.bmp"
]
caseMode = False
caseIndex = 0

while True:
    cache=fr.readline()
    if cache=='':
        break
    cache=cache.strip()
    cache=cache.replace('\t', '')
    if cache=='':
        continue

    if not caseMode:
        if cache.startswith('//case'):
            # ignored item
            # skip this
            pass
        elif cache.startswith('case'):
            codeline = ""
            caseMode = True
            caseIndex=int(cache.split(' ')[1].replace(':', ''))
    else:
        if cache=='break;':
            codeline+=cache+"\n"
            caseMode = False
            caseDict[caseIndex] = codeline
        else:
            codeline+=cache+"\n"

fr.close()
fw=open('migrated.txt', 'w')

newList = [
    "atari.avi",
    "atari.bmp",
    "Ball_LightningSphere1.bmp",
    "Ball_LightningSphere2.bmp",
    "Ball_LightningSphere3.bmp",
    "Ball_Paper.bmp",
    "Ball_Stone.bmp",
    "Ball_Wood.bmp",
    "Brick.bmp",
    "Button01_deselect.tga",
    "Button01_select.tga",
    "Button01_special.tga",
    "Column_beige.bmp",
    "Column_beige_fade.tga",
    "Column_blue.bmp",
    "Cursor.tga",
    "Dome.bmp",
    "DomeEnvironment.bmp",
    "DomeShadow.tga",
    "ExtraBall.bmp",
    "ExtraParticle.bmp",
    "E_Holzbeschlag.bmp",
    "FloorGlow.bmp",
    "Floor_Side.bmp",
    "Floor_Top_Border.bmp",
    "Floor_Top_Borderless.bmp",
    "Floor_Top_Checkpoint.bmp",
    "Floor_Top_Flat.bmp",
    "Floor_Top_Profil.bmp",
    "Floor_Top_ProfilFlat.bmp",
    "Font_1.tga",
    "Gravitylogo_intro.bmp",
    "HardShadow.bmp",
    "Laterne_Glas.bmp",
    "Laterne_Schatten.tga",
    "Laterne_Verlauf.tga",
    "Logo.bmp",
    "Metal_stained.bmp",
    "Misc_Ufo.bmp",
    "Misc_UFO_Flash.bmp",
    "Modul03_Floor.bmp",
    "Modul03_Wall.bmp",
    "Modul11_13_Wood.bmp",
    "Modul11_Wood.bmp",
    "Modul15.bmp",
    "Modul16.bmp",
    "Modul18.bmp",
    "Modul18_Gitter.tga",
    "Modul30_d_Seiten.bmp",
    "Particle_Flames.bmp",
    "Particle_Smoke.bmp",
    "PE_Bal_balloons.bmp",
    "PE_Bal_platform.bmp",
    "PE_Ufo_env.bmp",
    "Pfeil.tga",
    "P_Extra_Life_Oil.bmp",
    "P_Extra_Life_Particle.bmp",
    "P_Extra_Life_Shadow.bmp",
    "Rail_Environment.bmp",
    "sandsack.bmp",
    "SkyLayer.bmp",
    "Sky_Vortex.bmp",
    "Stick_Bottom.tga",
    "Stick_Stripes.bmp",
    "Target.bmp",
    "Tower_Roof.bmp",
    "Trafo_Environment.bmp",
    "Trafo_FlashField.bmp",
    "Trafo_Shadow_Big.tga",
    "Tut_Pfeil01.tga",
    "Tut_Pfeil_Hoch.tga",
    "Wolken_intro.tga",
    "Wood_Metal.bmp",
    "Wood_MetalStripes.bmp",
    "Wood_Misc.bmp",
    "Wood_Nailed.bmp",
    "Wood_Old.bmp",
    "Wood_Panel.bmp",
    "Wood_Plain.bmp",
    "Wood_Plain2.bmp",
    "Wood_Raft.bmp"
]

counter = 0
for item in newList:
    if item in oldList:
        existedCode = caseDict.get(oldList.index(item), '')
    else:
        existedCode = ''
    if existedCode == '':
        fw.write('//')
    fw.write('case {}:    //{}'.format(counter, item))
    fw.write('\n')
    fw.write(existedCode)

    counter+=1

fw.close()