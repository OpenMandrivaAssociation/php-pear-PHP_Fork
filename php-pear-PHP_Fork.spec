%define		_class		PHP
%define		_subclass	Fork
%define		upstream_name	%{_class}_%{_subclass}

%define		_requires_exceptions pear(Snoopy.class.php)

Name:		php-pear-%{upstream_name}
Version:	0.3.1
Release:	%mkrel 3
Summary:	Wrapper for pcntl_fork() with Java-like API
License:	PHP License
Group:		Development/PHP
URL:		http://pear.php.net/package/PHP_Fork/
Source0:	http://download.pear.php.net/package/%{upstream_name}-%{version}.tgz
Requires(post): php-pear
Requires(preun): php-pear
Requires:	php-pear
Requires:	php-shmop
Requires:	php-pcntl
BuildArch:	noarch
BuildRequires:	php-pear
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
PHP_Fork class. Wrapper around the pcntl_fork() stuff with a API set
like Java language. Practical usage is done by extending this class,
and re-defining the run() method.

This way PHP developers can enclose logic into a class that extends
PHP_Fork, then execute the start() method that forks a child process.
Communications with the forked process is ensured by using a Shared
Memory Segment; by using a user-defined signal and this shared memory
developers can access to child process methods that returns a
serializable variable.

The shared variable space can be accessed with the two methods:
- void setVariable($name, $value)
- mixed getVariable($name)

$name must be a valid PHP variable name;
$value must be a variable or a serializable object.

Resources (db connections, streams, etc.) cannot be serialized and so
they're not correctly handled.

%prep
%setup -q -c
mv package.xml %{upstream_name}-%{version}/%{upstream_name}.xml

%install
rm -rf %{buildroot}

cd %{upstream_name}-%{version}
pear install --nodeps --packagingroot %{buildroot} %{upstream_name}.xml
rm -rf %{buildroot}%{_datadir}/pear/.??*

rm -rf %{buildroot}%{_datadir}/pear/docs
rm -rf %{buildroot}%{_datadir}/pear/tests

install -d %{buildroot}%{_datadir}/pear/packages
install -m 644 %{upstream_name}.xml %{buildroot}%{_datadir}/pear/packages

%clean
rm -rf %{buildroot}

%post
%if %mdkversion < 201000
pear install --nodeps --soft --force --register-only \
    %{_datadir}/pear/packages/%{upstream_name}.xml >/dev/null || :
%endif

%preun
%if %mdkversion < 201000
if [ "$1" -eq "0" ]; then
    pear uninstall --nodeps --ignore-errors --register-only \
        %{upstream_name} >/dev/null || :
fi
%endif

%files
%defattr(-,root,root)
%doc %{upstream_name}-%{version}/examples
%{_datadir}/pear/%{_class}
%{_datadir}/pear/packages/%{upstream_name}.xml
