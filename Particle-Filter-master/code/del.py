for i in range(numParticles):
    while (1):
        # XInitial[i] = np.array([3900, 4000, 0])
        XInitial[i] = np.array([np.random.uniform(0, global_mapsize_x), np.random.uniform(0, global_mapsize_y),
                                np.random.uniform(-1 * np.pi, np.pi)])
        occ = gridFunctions.occupancy(XInitial[i], resolution, mapData)
        if occ > 0.8:  # and occ>-1:
            break