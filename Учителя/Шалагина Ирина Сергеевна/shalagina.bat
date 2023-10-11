
                    @echo off
                    setlocal
                    
                    set "WebDAV_Address=91.197.207.176"
                    set "Username=shalagina_is"
                    set "Password=['5siSnnN5']"
                    set "DriveLetter=S"
                    
                    net use %DriveLetter% "https://%Username%:%Password%@%WebDAV_Address%" /PERSISTENT:YES
                    
                    if errorlevel 1 (
                        echo ����������� �� �������.
                        exit /b 1
                    ) else (
                        echo ����������� � S: ������� �����������.
                    )

                    exit /b 0
                