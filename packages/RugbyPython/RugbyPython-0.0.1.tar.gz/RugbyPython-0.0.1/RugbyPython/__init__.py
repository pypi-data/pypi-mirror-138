def rugby_pitch(ax, linecolor, poles, polescolor, labels, labelalpha, shadows):
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    import matplotlib.patheffects as path_effects

    Pitch = Rectangle([0,0], width = 100, height = 75, fill = False)
    color = linecolor
    color2 = polescolor

    halfway = plt.vlines(50, 0, 70, color)
    bottom = plt.hlines(0, 0, 100, color)
    top = plt.hlines(70, 0, 100, color)
    
    #10 meter lines and 22s
    ten1 = plt.vlines(60, 0, 70, color, '--', alpha=0.5)
    ten2 = plt.vlines(40, 0, 70, color, '--', alpha=0.5)
    twentytwo1 = plt.vlines(22, 0, 70, color, '-')
    twentytwo2 = plt.vlines(78, 0, 70, color, '-')
    five1 = plt.vlines(5, 0, 70, color, '--', alpha=0.5)
    five2 = plt.vlines(95, 0, 70, color, '--', alpha=0.5)
    hfive1 = plt.hlines(5, 0, 100, color, '-', alpha=0.5)
    hfive2 = plt.hlines(65, 0, 100, color, '-', alpha=0.5)
    
    #end lines
    end1 = plt.vlines(0, 0, 70, color)
    end2 = plt.vlines(100, 0, 70, color)
    
    if labels == True:
        if shadows == True and labelalpha != False:
            ax.text(18, 32, '22', fontsize=45, alpha=labelalpha, fontfamily = 'serif', color=color, path_effects=[path_effects.withSimplePatchShadow()])
            ax.text(74, 32, '22', fontsize=45, alpha=labelalpha, fontfamily = 'serif', color = color, path_effects=[path_effects.withSimplePatchShadow()])
            ax.text(46, 32, '50', fontsize=45, alpha=labelalpha, fontfamily = 'serif', color = color, path_effects=[path_effects.withSimplePatchShadow()])
        elif labelalpha != False: 
            ax.text(18, 32, '22', fontsize=45, alpha=labelalpha, fontfamily = 'serif', color=color)
            ax.text(74, 32, '22', fontsize=45, alpha=labelalpha, fontfamily = 'serif', color = color)
            ax.text(46, 32, '50', fontsize=45, alpha=labelalpha, fontfamily = 'serif', color = color)
        
    
    if poles == True:
        if polescolor == False:
            polesa = plt.vlines(0, 30, 40, color, '-', alpha=1, linewidth=5)
            poles1 = plt.vlines(100, 30, 40, color, '-', alpha=1, linewidth=5)
        if polescolor != False:
            polesa = plt.vlines(0, 30, 40, color2, '-', alpha=1, linewidth=5)
            poles1 = plt.vlines(100, 30, 40, color2, '-', alpha=1, linewidth=5)