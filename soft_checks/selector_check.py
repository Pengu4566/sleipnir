def selector_check(df_selector, fileLocationStr, df_json):
    df_selector_dup = df_selector.copy()
    df_json_dup = df_json.copy()

    df_selector_dup.filePath = df_selector_dup.filePath.str.replace(fileLocationStr, '')
    df_selector_dup.selectorStr = df_selector_dup.selectorStr.str.replace("\"", "'")
    # df_selector_dup.to_csv('./selectors.csv')

    if len(df_selector_dup.filePath) > 0:
        return list(df_selector_dup.reset_index(drop=True).reset_index().T.to_dict().values())
    else:
        return ['There is no selectors in your project.']