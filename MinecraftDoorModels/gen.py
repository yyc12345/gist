
angle_order = (0, 90, 180, 270)
angle_facing_maps = (0, 270, 90, 180)
facing_tuple = ("east", "north", "south", "west")
half_tuple = ("lower", "upper")
hinge_tuple = ("left", "right")
open_tuple = ("false", "true")
pos_tuple = ("bottom", "top")

door_types = ("iron", "oak", "spruce", "birch", "jungle", "acacia", "dark_oak", "mangrove", "crimson", "warped")

def get_y_from_types(_facing, _hinge, _open):
    init_angle = angle_facing_maps[facing_tuple.index(_facing)]
    # if open is false, return directly
    if _open == 'false':
        return init_angle

    # analyse open == true
    # if hinge == left, clockwise increase angle
    # else, countdown decrease angle
    angle_idx = angle_order.index(init_angle)
    if _hinge == 'left':
        angle_idx += 1
    else:
        angle_idx -= 1
        angle_idx += 4  # remove minus number
    angle_idx = angle_idx % 4
    return angle_order[angle_idx]

def half_to_bottomtop(_half):
    return pos_tuple[half_tuple.index(_half)]

for single_door in door_types:
    with open('blockstates/{}_door.json'.format(single_door), 'w', encoding='utf-8') as fblockstate:
        
        fblockstate.write('{\n"variants": {\n')
        is_first = True
        for half in half_tuple:
            for hinge in hinge_tuple:
                for mcopen in open_tuple:
                    # write models
                    bottom_or_top = half_to_bottomtop(half)
                    if mcopen == 'true':
                        openstr = '_open'
                    else:
                        openstr = ''

                    if mcopen == 'true':
                        suffixstr = '1'
                    else:
                        suffixstr = ''

                    # example: acacia_door_top_left_open
                    json_name = '{}_door_{}_{}{}{}'.format(single_door, bottom_or_top, hinge, openstr, suffixstr)

                    with open('models/block/{}.json'.format(json_name), 'w', encoding='utf-8') as fmodel:
                        fmodel.write('{\n')
                        fmodel.write('"parent": "minecraft:block/door_{}_{}{}",\n'.format(bottom_or_top, hinge, openstr))
                        fmodel.write('"textures": {\n')
                        fmodel.write('"bottom": "minecraft:block/{}_door_{}{}",\n'.format(single_door, bottom_or_top, suffixstr))
                        fmodel.write('"top": "minecraft:block/{}_door_{}{}"\n'.format(single_door, bottom_or_top, suffixstr))
                        fmodel.write('}\n}')

                    # write blockstates
                    for facing in facing_tuple:
                        if not is_first:
                            fblockstate.write(',')
                        else:
                            is_first = False

                        y = get_y_from_types(facing, hinge, mcopen)
                        if y == 0:
                            ystr = ''
                        else:
                            ystr = ',"y":{}'.format(y)

                        # example: minecraft:block/
                        fblockstate.write('\n"facing={},half={},hinge={},open={}":{{"model": "minecraft:block/{}"{}}}'.format(
                            facing, half, hinge, mcopen, json_name, ystr
                        ))

        fblockstate.write('\n}\n}')