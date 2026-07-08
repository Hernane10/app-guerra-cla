[app]
title = Controle de Guerras CR
package.name = guerrasclan
package.domain = br.dev.hernane
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3, kivy, urllib3
android.api = 33
android.minapi = 24
android.ndk = 25b
android.permissions = INTERNET
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1