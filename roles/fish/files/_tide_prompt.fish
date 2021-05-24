function _tide_prompt
    # Variables are exported as strings, convert _tide_last_pipestatus back into a list
    set -g _tide_last_pipestatus (string split ' ' $_tide_last_pipestatus)

    test "$tide_print_newline_before_prompt" = true && printf '%b' '\n'

    set -l leftPrompt (_tide_left_prompt)
    set -l leftPromptHeight (count $leftPrompt)
    set -l rightPrompt (_tide_right_prompt)

    for i in ( seq 1 $leftPromptHeight )

        printf '%s' $leftPrompt[$i]

        if test -n "$rightPrompt[$i]"
            set_color $tide_prompt_connection_color
            test -n "$tide_prompt_connection_icon" || set -l tide_prompt_connection_icon ' '
            set -l lengthToMove (math $COLUMNS - (_tide_decolor "$leftPrompt[1]""$rightPrompt[1]" | string length))
            test $lengthToMove -gt 0 && string repeat --no-newline --max $lengthToMove $tide_prompt_connection_icon

            printf '%s\n' $rightPrompt[$i]
        else
          printf ' \n'
        end
    end

    if test -n "$_tide_right_prompt_display_var";
        set -U -e $_tide_right_prompt_display_var;
    end;
end
