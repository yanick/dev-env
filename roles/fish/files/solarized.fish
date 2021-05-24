

function fish_solarized

    if contains set $argv
        echo "setting the colors"
        set -U solarized_base03  002b36
        set -U solarized_base02  073642
        set -U solarized_base01  586e75
        set -U solarized_base00  657b83
        set -U solarized_base0   839496
        set -U solarized_base1   93a1a1
        set -U solarized_base2   eee8d5
        set -U solarized_base3   fdf6e3
        set -U solarized_yellow  b58900
        set -U solarized_orange  cb4b16
        set -U solarized_red     dc322f
        set -U solarized_magenta d33682
        set -U solarized_violet  6c71c4
        set -U solarized_blue    268bd2
        set -U solarized_cyan    2aa198
        set -U solarized_green   859900
    end

    if test -z "$argv"
        set argv test
    end

    for color in ( set --names | grep solarized )
        printf "%-20s" $color
        echo " " ( set_color $$color ) $argv ( set_color normal ) \
            ( set_color --bold $$color ) $argv ( set_color normal ) \
            ( set_color --background $$color ) $argv ( set_color normal )

    end


end
