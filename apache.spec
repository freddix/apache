Summary:	High performance HTTP server
Name:		apache
Version:	2.4.7
Release:	1
License:	Apache
Group:		Networking/Daemons/HTTP
Source0:	http://www.apache.org/dist/httpd/httpd-%{version}.tar.bz2
# Source0-md5:	170d7fb6fe5f28b87d1878020a9ab94e
Source1:	%{name}.layout
BuildRequires:	apr-devel
BuildRequires:	apr-util-devel
BuildRequires:	autoconf
BuildRequires:	libtool
BuildRequires:	pcre-devel
BuildRequires:	pkg-config
BuildRequires:	zlib-devel
Requires(post,preun,postun):	systemd-units
Provides:	group(http)
Provides:	user(http)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_cgibindir	%{_prefix}/lib/cgi-bin/apache
%define		_datadir	/srv/www
%define		_includedir	%{_prefix}/include/apache
%define		_libexecdir	%{_libdir}/apache
%define		_sysconfdir	/etc/httpd/conf

%description
The Apache HTTP Server is a web server application notable for playing
a key role in the initial growth of the World Wide Web.

%package manual
Summary:	Apache manual
Group:		Documentation

%description manual
Apache manual.

%package devel
Summary:	Header files for ... library
Group:		Development/Libraries
#Requires:	%{name} = %{version}-%{release}

%description devel
This is the package containing the header files for ... library.

%prep
%setup -qn httpd-%{version}

cat %{SOURCE1} >> config.layout

%ifarch x8664
%{__sed} -i -e 's,/lib$,/%{_lib},' config.layout
%endif

%build
%{__libtoolize}
%{__aclocal} -I build
%{__autoconf}
%{__autoheader}
%configure \
	--enable-layout=Freddix
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
#install -d $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT%{_sysconfdir}/{extra,conf.d}

ln -s %{_libexecdir} $RPM_BUILD_ROOT%{_sysconfdir}/modules
ln -s /run/httpd $RPM_BUILD_ROOT%{_sysconfdir}/run
ln -s %{_var}/log/httpd $RPM_BUILD_ROOT%{_sysconfdir}/logs

# cleanup
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/manual/style/{lang,latex,xsl}
find $RPM_BUILD_ROOT%{_datadir}/manual/style -type f ! -name '*.css' -print0 | xargs -0r rm -f
%{__rm} $RPM_BUILD_ROOT%{_libexecdir}/build/config.nice
%{__rm} $RPM_BUILD_ROOT%{_libexecdir}/*.exp
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/mime.types
%{__rm} -r $RPM_BUILD_ROOT%{_sysconfdir}/original

# find manual files
> manual.files
cur=$(pwd)
cd $RPM_BUILD_ROOT
find ./%{_datadir}/manual -type d -printf "%%%%dir %{_datadir}/manual/%%P\n" >> "$cur/manual.files"
find ./%{_datadir}/manual -type f -printf "%{_datadir}/manual/%%P\n" | sed -e '
s/^.*\.\(de\|es\|fr\|ja\|ko\|ru\)\(\..*\)\?/%%lang(\1) &/
s/^.*\.\(pt-br\)/%%lang(pt_BR) &/
' >> "$cur/manual.files"
cd $cur

%clean
rm -rf $RPM_BUILD_ROOT

%pre

%post

%preun

%postun

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ab
%attr(755,root,root) %{_bindir}/htdigest
%attr(755,root,root) %{_bindir}/logresolve
%attr(755,root,root) %{_bindir}/dbmmanage
%attr(755,root,root) %{_bindir}/htdbm
%attr(755,root,root) %{_bindir}/htpasswd
%attr(755,root,root) %{_bindir}/httxt2dbm

%attr(755,root,root) %{_sbindir}/apachectl
%attr(755,root,root) %{_sbindir}/checkgid
%attr(755,root,root) %{_sbindir}/httpd
%attr(755,root,root) %{_sbindir}/rotatelogs
%attr(755,root,root) %{_sbindir}/fcgistarter
%attr(755,root,root) %{_sbindir}/htcacheclean

%dir %{_libexecdir}
%attr(755,root,root) %{_libexecdir}/mod_access_compat.so
%attr(755,root,root) %{_libexecdir}/mod_actions.so
%attr(755,root,root) %{_libexecdir}/mod_alias.so
%attr(755,root,root) %{_libexecdir}/mod_allowmethods.so
%attr(755,root,root) %{_libexecdir}/mod_auth_basic.so
%attr(755,root,root) %{_libexecdir}/mod_auth_digest.so
%attr(755,root,root) %{_libexecdir}/mod_auth_form.so
%attr(755,root,root) %{_libexecdir}/mod_authn_anon.so
%attr(755,root,root) %{_libexecdir}/mod_authn_core.so
%attr(755,root,root) %{_libexecdir}/mod_authn_dbd.so
%attr(755,root,root) %{_libexecdir}/mod_authn_dbm.so
%attr(755,root,root) %{_libexecdir}/mod_authn_file.so
%attr(755,root,root) %{_libexecdir}/mod_authn_socache.so
%attr(755,root,root) %{_libexecdir}/mod_authz_core.so
%attr(755,root,root) %{_libexecdir}/mod_authz_dbd.so
%attr(755,root,root) %{_libexecdir}/mod_authz_dbm.so
%attr(755,root,root) %{_libexecdir}/mod_authz_groupfile.so
%attr(755,root,root) %{_libexecdir}/mod_authz_host.so
%attr(755,root,root) %{_libexecdir}/mod_authz_owner.so
%attr(755,root,root) %{_libexecdir}/mod_authz_user.so
%attr(755,root,root) %{_libexecdir}/mod_autoindex.so
%attr(755,root,root) %{_libexecdir}/mod_buffer.so
%attr(755,root,root) %{_libexecdir}/mod_cache.so
%attr(755,root,root) %{_libexecdir}/mod_cache_disk.so
%attr(755,root,root) %{_libexecdir}/mod_cache_socache.so
%attr(755,root,root) %{_libexecdir}/mod_cgid.so
%attr(755,root,root) %{_libexecdir}/mod_dav.so
%attr(755,root,root) %{_libexecdir}/mod_dav_fs.so
%attr(755,root,root) %{_libexecdir}/mod_dbd.so
%attr(755,root,root) %{_libexecdir}/mod_deflate.so
%attr(755,root,root) %{_libexecdir}/mod_dir.so
%attr(755,root,root) %{_libexecdir}/mod_dumpio.so
%attr(755,root,root) %{_libexecdir}/mod_env.so
%attr(755,root,root) %{_libexecdir}/mod_expires.so
%attr(755,root,root) %{_libexecdir}/mod_ext_filter.so
%attr(755,root,root) %{_libexecdir}/mod_file_cache.so
%attr(755,root,root) %{_libexecdir}/mod_filter.so
%attr(755,root,root) %{_libexecdir}/mod_headers.so
%attr(755,root,root) %{_libexecdir}/mod_include.so
%attr(755,root,root) %{_libexecdir}/mod_info.so
%attr(755,root,root) %{_libexecdir}/mod_lbmethod_bybusyness.so
%attr(755,root,root) %{_libexecdir}/mod_lbmethod_byrequests.so
%attr(755,root,root) %{_libexecdir}/mod_lbmethod_bytraffic.so
%attr(755,root,root) %{_libexecdir}/mod_lbmethod_heartbeat.so
%attr(755,root,root) %{_libexecdir}/mod_log_config.so
%attr(755,root,root) %{_libexecdir}/mod_log_debug.so
%attr(755,root,root) %{_libexecdir}/mod_logio.so
%attr(755,root,root) %{_libexecdir}/mod_macro.so
%attr(755,root,root) %{_libexecdir}/mod_mime.so
%attr(755,root,root) %{_libexecdir}/mod_negotiation.so
%attr(755,root,root) %{_libexecdir}/mod_ratelimit.so
%attr(755,root,root) %{_libexecdir}/mod_remoteip.so
%attr(755,root,root) %{_libexecdir}/mod_reqtimeout.so
%attr(755,root,root) %{_libexecdir}/mod_request.so
%attr(755,root,root) %{_libexecdir}/mod_rewrite.so
%attr(755,root,root) %{_libexecdir}/mod_sed.so
%attr(755,root,root) %{_libexecdir}/mod_setenvif.so
%attr(755,root,root) %{_libexecdir}/mod_slotmem_shm.so
%attr(755,root,root) %{_libexecdir}/mod_socache_dbm.so
%attr(755,root,root) %{_libexecdir}/mod_socache_memcache.so
%attr(755,root,root) %{_libexecdir}/mod_socache_shmcb.so
%attr(755,root,root) %{_libexecdir}/mod_speling.so
%attr(755,root,root) %{_libexecdir}/mod_status.so
%attr(755,root,root) %{_libexecdir}/mod_substitute.so
%attr(755,root,root) %{_libexecdir}/mod_unique_id.so
%attr(755,root,root) %{_libexecdir}/mod_unixd.so
%attr(755,root,root) %{_libexecdir}/mod_userdir.so
%attr(755,root,root) %{_libexecdir}/mod_version.so
%attr(755,root,root) %{_libexecdir}/mod_vhost_alias.so

%attr(755,root,root) %{_libexecdir}/mod_ssl.so

%attr(755,root,root) %{_libexecdir}/mod_proxy.so
%attr(755,root,root) %{_libexecdir}/mod_proxy_ajp.so
%attr(755,root,root) %{_libexecdir}/mod_proxy_balancer.so
%attr(755,root,root) %{_libexecdir}/mod_proxy_connect.so
%attr(755,root,root) %{_libexecdir}/mod_proxy_express.so
%attr(755,root,root) %{_libexecdir}/mod_proxy_fcgi.so
%attr(755,root,root) %{_libexecdir}/mod_proxy_ftp.so
%attr(755,root,root) %{_libexecdir}/mod_proxy_http.so
%attr(755,root,root) %{_libexecdir}/mod_proxy_scgi.so
%attr(755,root,root) %{_libexecdir}/mod_proxy_wstunnel.so

%attr(755,root,root) %{_libexecdir}/mod_session.so
%attr(755,root,root) %{_libexecdir}/mod_session_cookie.so
%attr(755,root,root) %{_libexecdir}/mod_session_dbd.so

%{_datadir}/icons
%{_datadir}/error

%{_mandir}/man1/ab.1*
%{_mandir}/man1/dbmmanage.1*
%{_mandir}/man1/htdbm.1*
%{_mandir}/man1/htdigest.1*
%{_mandir}/man1/htpasswd.1*
%{_mandir}/man1/httxt2dbm.1*
%{_mandir}/man1/logresolve.1*
%{_mandir}/man8/apachectl.8*
%{_mandir}/man8/fcgistarter.8*
%{_mandir}/man8/htcacheclean.8*
%{_mandir}/man8/httpd.8*
%{_mandir}/man8/rotatelogs.8*
%{_mandir}/man8/suexec.8*

%dir %{_cgibindir}
%attr(755,root,root) %{_cgibindir}/*

%attr(751,root,root) %dir %{_sysconfdir}
%attr(750,root,root) %dir %{_sysconfdir}/conf.d
%attr(640,root,root) %{_sysconfdir}/magic
%{_sysconfdir}/logs
%{_sysconfdir}/modules
%{_sysconfdir}/run

%files manual -f manual.files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/httpd-manual.conf

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/apxs
%attr(755,root,root) %{_sbindir}/envvars*
%{_includedir}
%dir %{_libexecdir}
%dir %{_libexecdir}/build
%attr(755,root,root) %{_libexecdir}/build/*.sh
%{_libexecdir}/build/[lprs]*.mk
%{_libexecdir}/build/config_vars.mk
%{_mandir}/man1/apxs.1*

%if 0
%doc AUTHORS ChangeLog NEWS README TODO
# if _sysconfdir != /etc:
#%%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%endif

# initscript and its config
%if %{with initscript}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%endif

#%{_examplesdir}/%{name}-%{version}

%if %{with subpackage}
%files subpackage
%defattr(644,root,root,755)
#%doc extras/*.gz
#%{_datadir}/%{name}-ext
%endif
