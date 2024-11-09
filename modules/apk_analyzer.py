import config

def apk_analysis_from_device(user_input):
    '''
        APK Analysis
        - apk extraction from the mobile device or on the pc
        - apk decoding with apktool
        java -jar 
    '''
    pass

def apk_analysis_from_file(user_input):
    '''
        APK Analysis
        - apk extraction from the mobile device or on the pc
        - apk decoding with apktool
        java -jar 
    '''
    pass

def apk_decompiler_from_device(user_input):
    # Decompile the program
    # apktool d APP.apk -o <dir>
    pass

def apk_decompiler_from_file(user_input):
    # Decompile the program
    # apktool d APP.apk -o <dir>
    pass

def jar_from_device(user_input):
    # Decompile the program
    # apktool d APP.apk -o <dir>
    pass

def jar_from_file(user_input):
    # Decompile the program
    # apktool d APP.apk -o <dir>
    pass


def jadx_from_device(user_input):
    # Decompile the program
    # apktool d APP.apk -o <dir>
    pass

def jadx_from_file(user_input):
    # Decompile the program
    # apktool d APP.apk -o <dir>
    pass

def apk_compile_from_folder(user_input):
    # Decompile the program
    # apktool b <folder>
    # The final modded app will be in the "dist" folder located inside the original app folder created by apktool.
    # Zipalign is a zip archive alignment tool that helps ensure that all uncompressed files in the archive are aligned
    # relative to the start of the file. Zipalign tool can be found in the “Build Tools” folder within the Android SDK path.
    # zipalign -v 4 <recompiled_apk.apk> <zipaligned_apk.apk>
    # Create a new keystore file for signing the zip aligned APK
    # keytool -genkey -v -keystore <keystore_name> -alias alias_name -keyalg RSA -keysize 2048 -validity 10000
    # Use keystore file for signing the zip aligned APK
    # apksigner sign --ks <keystore_name> --v1-signing-enabled true --v2-signing-enabled true <zip_aligned_apk.apk>

    pass