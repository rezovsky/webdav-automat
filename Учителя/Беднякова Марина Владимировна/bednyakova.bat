
                    @echo off
                    setlocal
                    
                    set "WebDAV_Address=91.197.207.176"
                    set "Username=bednyakova_mv"
                    set "Password=['4bmVvnN7']"
                    set "DriveLetter=S"
                    
                    net use %DriveLetter% "https://%Username%:%Password%@%WebDAV_Address%" /PERSISTENT:YES
                    
                    if errorlevel 1 (
                        echo ����������� �� �������.
                        exit /b 1
                    ) else (
                        echo ����������� � S: ������� �����������.
                    )

                    exit /b 0
                