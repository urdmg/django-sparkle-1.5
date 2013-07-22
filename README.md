# django-sparkle

Django-sparkle is a Django application to make it easy to publish updates for your mac application using [sparkle](http://sparkle.andymatuschak.org/).

In addition to publishing updates via the appcast feed, Django-sparkle can also collect system profile information if sparkle is configured to report it.

# Requirements

* Django >= 1.5
* OpenSSL
* Markdown (For release notes)

# Setup

1. `easy_install django-sparkle` or `pip install django-sparkle`
2. Add `sparkle` to your installed apps
3. In `settings.py` add `SPARKLE_PRIVATE_KEY_PATH` which is the path to your private DSA key for signing your releases.
4. In `urls.py` include the sparkle URLs by adding something like `(r'^sparkle/', include('sparkle.urls'))`.
5. Ensure your domain name is properly configured in the sites framework and `MEDIA_URL` is correctly set
6. `python manage.py syncdb` to create the tables needed for sparkle.

# Usage

Create an application and optionally add some versions.

The application's appcast feed will be available at `/whatever_you/configured_in/your_urls_py/(?P<application_id>\d+)/appcast.xml`.

Set the `SUFeedURL` key in your Info.plist to point to the sparkle application's appcast URL. `http://example.com/sparkle/1/appcast.xml` for example.

If you want to enable system profiling, be sure to set the `SUEnableSystemProfiling` key in your Info.plist to `YES`.

# Settings

`SPARKLE_PRIVATE_KEY_PATH`

The path to your DSA private key for signing releases.  Defaults to `None`.  If not provided, releases will not be automatically signed when uploaded.

# To Do

* Tests of course!

# License

This software is licensed under the terms of the BSD license:

Copyright (c) 2011, Jason Emerick  
Copyright (c) 2013, Johannes Spielmann  
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

 * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
 * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.