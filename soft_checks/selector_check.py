def selector_check(df_selector):
    df_selector_dup = df_selector.copy()
    df_selector_dup.to_csv('test.csv')
    df_selector_dup.fillna("Unknown", inplace=True)
    df_selector_dup['filePath'] = df_selector_dup.apply(lambda x: x['filePath'].replace(str(x['mainFolder']), ''), axis=1)
    df_selector_dup.selectorStr = df_selector_dup.selectorStr.str.replace("\"", "'")

    if len(df_selector_dup.filePath) > 0:
        return list(df_selector_dup.loc[:, ['selectorStr', 'filePath', 'projectName']]
                    .reset_index(drop=True).reset_index().T.to_dict().values())
    else:
        return []