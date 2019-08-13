def selector_check(df_selector, fileLocationStr, df_json_exp):
    df_selector_dup = df_selector.copy()
    df_json_exp_dup = df_json_exp.copy()
    df_selector_dup = df_selector_dup.merge(df_json_exp_dup, on=['filePath'], how='left')
    df_selector_dup.fillna("Unknown", inplace=True)
    df_selector_dup.filePath = df_selector_dup.filePath.str.replace(fileLocationStr, '')
    df_selector_dup.selectorStr = df_selector_dup.selectorStr.str.replace("\"", "'")
    # df_selector_dup.to_csv('./selectors.csv')

    if len(df_selector_dup.filePath) > 0:
        return list(df_selector_dup.reset_index(drop=True).reset_index().T.to_dict().values())
    else:
        return ['There is no selectors in your project.']