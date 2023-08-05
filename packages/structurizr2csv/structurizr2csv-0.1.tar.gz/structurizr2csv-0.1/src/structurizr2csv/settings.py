from structurizr2csv.enums import EdgeStyle

DOCKER_MOUNT_TARGET = "/structurizr2csv"

# This must match the workdir of the official structurizr/cli image
DOCKER_STRUCTURIZR_MOUNT_TARGET = "/usr/local/structurizr"

EDGE_STYLE = EdgeStyle.DIRECT

PRIMARY_GROUP_PADDING = 20
PRIMARY_GROUP_BOTTOM_PADDING = 60

SECONDARY_GROUP_PADDING = 10
SECONDARY_GROUP_BOTTOM_PADDING = 40

LEGEND_OFFSET_FROM_TITLE = 20

# Arbitrary sizing factor to adapt the positions so that the result layout looks OK.
# Structurizr diagrams are sized for 300 dpi, diagrams.net a priori for 100 dpi, but
# 0.33 will give bad results because the boxes' dimensions are not the same.
POSITION_FACTOR = 0.4

FILL_COLORS = {
    "person": "#083F75",
    "person-external": "#6C6477",
    "softwareSystem": "#1061B0",
    "softwareSystem-external": "#8C8496",
    "softwareSystem-existing": "#8C8496",
    "container": "#23A2D9",
    "container-external": "#8C8496",
    "component": "#63BEF2",
    "component-external": "#8C8496",
}
STROKE_COLORS = {
    "person": "#06315C",
    "person-external": "#4D4D4D",
    "softwareSystem": "#0D5091",
    "softwareSystem-external": "#736782",
    "softwareSystem-existing": "#736782",
    "container": "#0E7DAD",
    "container-external": "#8C8496",
    "component": "#2086C9",
    "component-external": "#8C8496",
}
