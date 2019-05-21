# Nichollette Acosta


def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes


def infotodict(seqinfo):
    # create directories

    # anathttps://www.youtube.com/watch?v=JRhV8YoEUqA/
    t1 = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_T1w')


    # fmap/
    fmap_phase = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_phasediff')
    fmap_magnitude = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_magnitude')


    # func/
    rest = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-resting_bold')


    info = {t1: [],  fmap_phase: [], rest: [],   fmap_magnitude: []}
    for s in seqinfo:
        print(s)
        if ("t1" in s.protocol_name) and (s.dim2==512):
            info[t1].append(s.series_id)  ## append if multiple series meet criteria
        try:
            if (s.dim3 == 36) and ('fmap' in s.protocol_name or 'gre' in s.protocol_name):
                info[fmap_phase].append(s.series_id)  ## append if multiple series meet criteria
            if (s.dim3 == 72) and ('fmap' in s.protocol_name or 'gre' in s.protocol_name):
                info[fmap_magnitude].append(s.series_id)  # append if multiple series meet criteria
        except:
            pass
        if ('resting' in s.protocol_name):
            info[rest].append(s.series_id)  # append if multiple series meet criteria



    return info