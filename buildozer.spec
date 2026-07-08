[app]
title = Controle de Guerras CR
package.name = guerrasclan
package.domain = br.dev.hernane
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3==3.10,kivy==2.3.0,urllib3
android.api = 33
android.minapi = 24
android.ndk = 25b
android.ndk_api = 24
android.permissions = INTERNET
android.archs = arm64-v8a, armeabi-v7a
android.enable_androidx = True
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
