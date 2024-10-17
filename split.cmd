@echo off
setlocal enabledelayedexpansion

REM Check if all required parameters are provided
if "%~4"=="" (
    echo Usage: %0 "input_image" rows columns "output_directory"
    echo Example: %0 "C:\My Images\input.jpg" 3 3 "C:\My Images\Output"
    exit /b 1
)

REM Assign parameters to variables
set "input_image=%~1"
set "rows=%~2"
set "columns=%~3"
set "output_dir=%~4"

REM Create output directory if it doesn't exist
if not exist "%output_dir%" mkdir "%output_dir%"

REM Get image dimensions
for /f "tokens=1-2" %%a in ('magick identify -format "%%w %%h" "%input_image%"') do (
    set "width=%%a"
    set "height=%%b"
)

REM Calculate tile dimensions
set /a "tile_width=width / columns"
set /a "tile_height=height / rows"

REM Calculate total number of tiles
set /a "total_tiles=rows * columns"

REM Split the image
set "tile_index=0"
for /l %%y in (%rows%,-1,1) do (
    for /l %%x in (1,1,%columns%) do (
        set /a "tile_index+=1"
        set /a "x_offset=(%%x - 1) * tile_width"
        set /a "y_offset=(%%y - 1) * tile_height"
        
        REM Pad tile_index to 3 digits
        set "padded_index=00!tile_index!"
        set "padded_index=!padded_index:~-3!"
        
        magick "%input_image%" -crop %tile_width%x%tile_height%+!x_offset!+!y_offset! "%output_dir%\tile_!padded_index!.png"
    )
)

del "%TEMP%\magick-*"

echo Image split into %total_tiles% tiles. Output saved in "%output_dir%".