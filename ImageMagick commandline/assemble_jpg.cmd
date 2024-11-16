@echo off
setlocal enabledelayedexpansion

REM Check if all required parameters are provided
if "%~4"=="" (
    echo Usage: %0 "input_directory" rows columns "output_image"
    echo Example: %0 "C:\My Images\Tiles\tile_" 3 3 "C:\My Images\assembled.jpg"
    echo Note: Image numbering should be 0-based
    exit /b 1
)

REM Assign parameters to variables
set "input_dir=%~1"
set "rows=%~2"
set "columns=%~3"
set "output_image=%~4"

REM Calculate total number of tiles
set /a "total_tiles=rows * columns"

REM Create a blank black tile
magick -size 100x100 xc:black "%TEMP%\black_tile.jpg"

REM Build the montage command
set "montage_cmd=magick montage"
for /l %%y in (%rows%,-1,1) do (
    for /l %%x in (1,1,%columns%) do (
        set /a "tile_index=((%%y-1)*%columns%-1) + %%x"
        set "padded_index=00!tile_index!"
        set "padded_index=!padded_index:~-3!"
        if exist "%input_dir%!padded_index!.jpg" (
            set "montage_cmd=!montage_cmd! "%input_dir%!padded_index!.jpg""
        ) else (
            echo Warning: %input_dir%!padded_index!.jpg not found. Using black tile instead.
            set "montage_cmd=!montage_cmd! "%TEMP%\black_tile.jpg""
        )
    )
)

REM Complete the montage command
set "montage_cmd=!montage_cmd! -geometry +0+0 -tile %columns%x%rows% "%output_image%_qs%columns%x%rows%a0.5625.jpg""

REM Execute the montage command
%montage_cmd%

if %errorlevel% equ 0 (
    echo Images assembled successfully. Output saved as "%output_image%".
) else (
    echo Error occurred while assembling images.
)

REM Clean up temporary files
del "%TEMP%\black_tile.jpg"
del "%TEMP%\magick-*"