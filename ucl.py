

last_16 = [None] * 16
group_winners = []
runner_ups = []
pairs = [None] * 8

def create_team_dict(name, group, rank, association): 
    team = dict.fromkeys(["name", "group", "rank", "association"])

    team["name"] = name
    team["group"] = group
    team["rank"] = rank
    team["association"] = association

    return team

def create_default_last_16(): 
    last_16[0] = create_team_dict("Man City", "A", 1, "England")
    last_16[1] = create_team_dict("PSG", "A", 2, "France")
    last_16[2] = create_team_dict("Liverpool", "B", 1, "England")
    last_16[3] = create_team_dict("Atletico Madrid", "B", 2, "Spain")
    last_16[4] = create_team_dict("Ajax", "C", 1, "Netherlands")
    last_16[5] = create_team_dict("Sporting CP", "C", 2, "Portugal")
    last_16[6] = create_team_dict("Real Madrid", "D", 1, "Spain")
    last_16[7] = create_team_dict("Inter Milan", "D", 2, "Italy")
    last_16[8] = create_team_dict("Bayern Munich", "E", 1, "Germany")
    last_16[9] = create_team_dict("Benfica", "E", 2, "Portugal")
    last_16[10] = create_team_dict("Man United", "F", 1, "England")
    last_16[11] = create_team_dict("Villarreal", "F", 2, "Spain")
    last_16[12] = create_team_dict("Lille", "G", 1, "France")
    last_16[13] = create_team_dict("RB Salzburg", "G", 2, "Austria")
    last_16[14] = create_team_dict("Juventus", "H", 1, "Italy")
    last_16[15] = create_team_dict("Chelsea", "H", 2, "England")

    for team in last_16: 
        if team["rank"] == 1: 
            group_winners.append(team)
        else: 
            runner_ups.append(team)

def check_runner_up_draw(team_name): 
    for runner_up in runner_ups: 
        if runner_up["name"].lower() == team_name.lower(): 
            drawn_team = runner_up

    if "drawn_team" in locals(): 
        return drawn_team
    else:
        print_dict(runner_ups, "Wrong team name entered! Please choose from the following: ")
        return None

def check_group_winner_draw(team_name, potential_opponents): 
    for potential_opponent in potential_opponents: 
        if potential_opponent["name"].lower() == team_name.lower(): 
            drawn_team = potential_opponent

    if "drawn_team" in locals(): 
        return drawn_team
    else:
        print_dict(group_winners, "Wrong team name entered! Please choose from the following: ")
        return None

def check_potential_opponents(drawn_runner_up, group_winner_list = group_winners): 
    potential_opponents = []
    impossible_opponents = []

    for group_winner in group_winner_list: 
        different_group_and_association = check_group_and_association(drawn_runner_up, group_winner)
        next_draw_possible = check_next_draw(drawn_runner_up, group_winner)

        if different_group_and_association and next_draw_possible: 
            potential_opponents.append(group_winner)
        else: 
            impossible_opponents.append(group_winner)

    # Add already paired group winners as impossible opponents
    for i in range(8): 
        try: 
            impossible_opponents.append(pairs[i][1])
        except TypeError: 
            pass

    return potential_opponents, impossible_opponents

def check_group_and_association(runner_up, group_winner): 
    if group_winner["group"] != runner_up["group"] and group_winner["association"] != runner_up["association"]: 
        return True
    else: 
        return False
        
def check_next_draw(current_runner_up, current_group_winner): 
    group_winners_temp = group_winners.copy()
    runner_ups_temp = runner_ups.copy()

    runner_ups_temp.remove(current_runner_up)
    group_winners_temp.remove(current_group_winner)

    if runner_ups_temp: 
        # Check if all runner-ups have at least one possible opponent
        for next_runner_up in runner_ups_temp: 
            # Check one runner-up
            this_runner_up_possible = False

            for next_group_winner in group_winners_temp: 
                this_runner_up_possible = check_group_and_association(next_runner_up, next_group_winner)
                if this_runner_up_possible: 
                    break
                else: 
                    continue
            
            if not this_runner_up_possible: 
                return False

        return True
    else: 
        return True

def print_dict(teams, description): 
    print("\n\n" + description)
    for team in teams: 
        print(f"{team['name']}")
    print("\n")

def main(): 
    create_default_last_16()
    print_dict(last_16, "Last 16 teams: ")

    draw_count = 1

    while(draw_count <= 8): 
        drawn_runner_up_name = input(f"Please enter runner-up draw No.{draw_count}: ")
        drawn_runner_up = check_runner_up_draw(drawn_runner_up_name)

        if drawn_runner_up is None: 
            continue

        potential_opponents, impossible_opponents = check_potential_opponents(drawn_runner_up)
        print_dict(potential_opponents, "Potential opponents: ")
        print_dict(impossible_opponents, "Impossible opponents: ")

        drawn_group_winner_name = input(f"Please enter group winner draw No.{draw_count}: ")
        drawn_group_winner = check_group_winner_draw(drawn_group_winner_name, potential_opponents)

        if drawn_group_winner is None: 
            continue

        pairs[draw_count - 1] = [drawn_runner_up, drawn_group_winner]
        print(f"\n\n{pairs[draw_count - 1][0]['name']} vs {pairs[draw_count - 1][1]['name']} confirmed!\n\n")
        
        runner_ups.remove(drawn_runner_up)
        group_winners.remove(drawn_group_winner)

        print_dict(group_winners, "Remaining group winners: ")
        print_dict(runner_ups, "Remaining runner-ups: ")

        draw_count += 1

    print("Draw result: ")
    for i in range(8): 
        print(f"{pairs[i][0]['name']} vs {pairs[i][1]['name']}")

    print("Draw completed!")

if __name__ == "__main__": 
    main()