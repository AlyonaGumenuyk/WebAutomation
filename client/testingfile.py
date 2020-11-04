import json
from pprint import pprint
from jsondiff import diff


class DiffStat:
    def __init__(self):
        self.result = {}

    def diff(self, prev_stats: dict, cur_stats: dict):
        self.result = {}
        try:
            score_result = self.diff_score(prev_stat=prev_stats, cur_stat=cur_stats)
            if score_result:
                self.result.update({'score_changes': score_result})
        except Exception as err:
            print(repr(err))
            pass

        try:
            dashboard_result = self.diff_dashboard_coefs(prev_stat=prev_stats, cur_stat=cur_stats)
            if dashboard_result:
                self.result.update({'dashboard_changed': dashboard_result})
        except Exception as err:
            print(repr(err))
            pass

        try:
            table_result = self.diff_table_coefs(prev_stat=prev_stats, cur_stat=cur_stats)
            if table_result:
                self.result.update({'table_reslut': table_result})
        except Exception as err:
            print(repr(err))
            pass

        try:
            status_result = self.diff_time(prev_stat=prev_stats, cur_stat=cur_stats)
            if self.result or 'status' in status_result:
                self.result.update({'status_changes': status_result})
        except Exception as err:
            print(repr(err))
            pass

        return self.result

    @staticmethod
    def diff_score(prev_stat: dict, cur_stat: dict):
        prev_score = prev_stat['score']
        cur_score = cur_stat['score']

        unfiltered_result_dict = {}

        prev_left_score = prev_score['command_left_score']
        cur_left_score = cur_score['command_left_score']

        prev_right_score = prev_score['command_right_score']
        cur_right_score = cur_score['command_right_score']

        if prev_left_score != cur_left_score:
            unfiltered_result_dict.update({'command_left_score_update': cur_left_score})

        if prev_right_score != cur_right_score:
            unfiltered_result_dict.update({'command_right_score_update': cur_right_score})

        result_dict = {k: v for k, v in unfiltered_result_dict.items() if v}

        return unfiltered_result_dict

    @staticmethod
    def diff_dashboard_coefs(prev_stat: dict, cur_stat: dict):
        prev_dashboard_coefs = prev_stat['dashboard_coefs']
        cur_dashboard_coefs = cur_stat['dashboard_coefs']

        # Поиск ключей в обоих словарях
        prev_stat_keys = prev_dashboard_coefs.keys()
        cur_stat_keys = cur_dashboard_coefs.keys()

        unfiltered_result_dict = {'command_left_changes': {}, 'command_right_changes': {}}

        # Поиск общих коэффициентов
        common_coefs = list(set(prev_stat_keys) & set(cur_stat_keys))

        # Поиск внесенных, удаленных и измененных коэффициентов по каждой группе
        for coef in common_coefs:
            prev_coef_value_left = prev_dashboard_coefs[coef]['command_left']
            cur_coef_value_left = cur_dashboard_coefs[coef]['command_left']

            prev_coef_value_right = prev_dashboard_coefs[coef]['command_right']
            cur_coef_value_right = cur_dashboard_coefs[coef]['command_right']

            if prev_coef_value_left != cur_coef_value_left:
                unfiltered_result_dict['command_left_changes'].update({coef: cur_coef_value_left})

            if prev_coef_value_right != cur_coef_value_right:
                unfiltered_result_dict['command_right_changes'].update({coef: cur_coef_value_right})

        result_dict = {k: v for k, v in unfiltered_result_dict.items() if v}

        return result_dict

    @staticmethod
    def diff_cards_and_penalties(prev_stat: dict, cur_stat: dict):
        prev_cards = prev_stat['cards_and_penalties']
        cur_cards = cur_stat['cards_and_penalties']

        unfiltered_result_dict = {}

        inserted_groups = {'command_left': {}, 'command_right': {}}
        deleted_groups = {'command_left': [], 'command_right': []}
        changed_groups = {'command_left': {}, 'command_right': {}}

        for command in ['command_left', 'command_right']:
            for group, value in cur_cards[command].items():
                if not prev_cards[command].get(group):
                    inserted_groups[command].update({group: value})
                elif prev_cards[command][group] != cur_cards[command][group]:
                    if command == 'command_left':
                        changed_groups['command_left'].update({group: value})
                    elif command == 'command_right':
                        changed_groups['command_right'].update({group: value})

            for group, value in prev_cards[command].items():
                if not cur_cards[command].get(group):
                    deleted_groups[command].append(group)

        result_dict = {}
        for group_dict in [(inserted_groups, 'inserted_groups'),
                           (deleted_groups, 'deleted_groups'),
                           (changed_groups, 'changed_groups')]:
            filtered_dict = ({k: v for k, v in group_dict[0].items() if v})
            if filtered_dict:
                result_dict.update({group_dict[1]: filtered_dict})
        return result_dict

    @staticmethod
    def diff_table_coefs(prev_stat: dict, cur_stat: dict):
        prev_table_coefs = prev_stat['table_coefs']
        cur_table_coefs = cur_stat['table_coefs']

        # Поиск ключей в обоих словарях
        prev_stat_keys = prev_table_coefs.keys()
        cur_stat_keys = cur_table_coefs.keys()

        unfiltered_result_dict = {'inserted_groups': {}, 'deleted_groups': [],
                                  'inserted_coefs': {}, 'deleted_coefs': {}, 'changed_coefs': {}}

        # Поиск внесенных групп коэффициентов
        inserted_groups = list(cur_stat_keys - prev_stat_keys)

        # Добавление всех внесенных групп и их коэффициентов в словарь внесенных групп
        for inserted_group in inserted_groups:
            unfiltered_result_dict['inserted_groups'].update({inserted_group: cur_table_coefs[inserted_group]})

        # Поиск удаленных групп коэффициентов
        deleted_groups = list(prev_stat_keys - cur_stat_keys)

        # Добавление всех удаленных групп и их коэффициентов в словарь удаленных групп
        for deleted_group in deleted_groups:
            unfiltered_result_dict['deleted_groups'].append(deleted_group)

        # Поиск общих групп к обоих словарях
        common_groups = list(set(prev_stat_keys) & set(cur_stat_keys))

        # Поиск внесенных, удаленных и измененных коэффициентов по каждой группе
        for group in common_groups:
            cur_stat_group_coefs = cur_table_coefs[group].keys()
            prev_stat_group_coefs = prev_table_coefs[group].keys()

            # Поиск внесенных, удаленных и общих коэффициентов в каждой группе
            inserted_coefs = list(cur_stat_group_coefs - prev_stat_group_coefs)
            deleted_coefs = list(prev_stat_group_coefs - cur_stat_group_coefs)
            common_coefs = list(set(cur_stat_group_coefs) & set(prev_stat_group_coefs))

            # Добавление внесенных коэффициентов группы в словарь
            inserted_coefs_dict = {}
            for inserted_coef in inserted_coefs:
                inserted_coefs_dict.update({inserted_coef: cur_table_coefs[group][inserted_coef]})
            if inserted_coefs_dict:
                unfiltered_result_dict['inserted_coefs'].update({group: inserted_coefs_dict})

            # Добавление удаленных коэффициентов группы в словарь
            deleted_coefs_dict = {}
            for deleted_coef in deleted_coefs:
                deleted_coefs_dict.update({deleted_coef: prev_table_coefs[group][deleted_coef]})
            if deleted_coefs_dict:
                unfiltered_result_dict['deleted_coefs'].update({group: deleted_coefs_dict})

            # Добавление измененных коэффициентов группы в словарь
            changed_coefs_dict = {}
            for coef in common_coefs:
                cur_coef_value = cur_table_coefs[group][coef]
                prev_coef_value = prev_table_coefs[group][coef]
                if cur_coef_value != prev_coef_value:
                    changed_coefs_dict.update({coef: cur_coef_value})
            if changed_coefs_dict:
                unfiltered_result_dict['changed_coefs'].update({group: changed_coefs_dict})

        result_dict = {k: v for k, v in unfiltered_result_dict.items() if v}

        return result_dict

    @staticmethod
    def diff_time(prev_stat: dict, cur_stat: dict):

        prev_current_status = prev_stat['current_status']
        cur_current_status = cur_stat['current_status']

        result_dict = {}

        prev_time = prev_current_status['time']
        cur_time = cur_current_status['time']

        prev_status = prev_current_status['status']
        cur_status = cur_current_status['status']

        if prev_status == cur_status:
            result_dict.update({'time': cur_time})
        elif prev_status != cur_status:
            result_dict.update({'status': cur_status,
                                'time': cur_time})

        return result_dict


prev = {'command_names': {'command_left': 'Arsenal', 'command_right': 'Manchester'},
        'score': {"command_left_score": 2, "command_right_score": 1},
        'current_status': {'status': 200, 'time': '19:10', 'period': 'Half1'},
        'dashboard_coefs': {'attack': {'command_left': 59, 'command_right': 52},
                            'defence': {'command_left': 47, 'command_right': 64}},
        'table_coefs': {'group1': {'win': 20, 'lose': 80},
                        'group2': {'total1': 10, 'total2': 20, 'total3': 45},
                        'group3': {'handicap': None}}}

cur = {'command_names': {'command_left': 'Arsenal', 'command_right': 'Manchester'},
       'score': {"command_left_score": 2, "command_right_score": 1},
       'current_status': {'status': 200, 'time': '19:10', 'period': 'Half1'},
       'dashboard_coefs': {'attack': {'command_left': 59, 'command_right': 52},
                           'defence': {'command_left': 47, 'command_right': 64}},
       'table_coefs': {'group1': {'win': 20, 'lose': 80},
                       'group2': {'total1': 10, 'total2': 20, 'total3': 45},
                       'group3': {'handicap': None}}}

prev_cards1 = {'cards_and_penalties': {'command_left': {'Corners': '1', 'Yellow cards': '2', 'Penalties': '0'},
                                       'command_right': {'Corners': '5', 'Yellow cards': '1'}}}
cur_cards1 = {'cards_and_penalties': {'command_left': {'Corners': '1', 'Yellow cards': '2', 'Penalties': '0'},
                                      'command_right': {'Corners': '5', 'Yellow cards': '1'}}}

diff_stat = DiffStat()
# result = diff_stat.diff(prev_stats=prev, cur_stats=cur)
result = diff_stat.diff_cards_and_penalties(prev_stat=prev_cards1, cur_stat=cur_cards1)
pprint(result)
