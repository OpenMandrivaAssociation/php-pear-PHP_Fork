%define		_class		PHP
%define		_subclass	Fork
%define		_status		beta
%define		_pearname	%{_class}_%{_subclass}

%define		_requires_exceptions pear(Snoopy.class.php)

Summary:	%{_pearname} - Wrapper for pcntl_fork() with Java-like API
Name:		php-pear-%{_pearname}
Version:	0.3.0
Release:	%mkrel 7
License:	PHP License
Group:		Development/PHP
Source0:	http://pear.php.net/get/%{_pearname}-%{version}.tar.bz2
URL:		http://pear.php.net/package/PHP_Fork/
Requires(post): php-pear
Requires(preun): php-pear
Requires:	php-pear
BuildArch:	noarch
BuildRequires:	dos2unix

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

In PEAR status of this package is: %{_status}.

%prep

%setup -q -c

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

# strip away annoying ^M
find -type f | grep -v ".gif" | grep -v ".png" | grep -v ".jpg" | xargs dos2unix -U

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_datadir}/pear/%{_class}

install %{_pearname}-%{version}/*.php %{buildroot}%{_datadir}/pear/%{_class}

install -d %{buildroot}%{_datadir}/pear/packages
install -m0644 package.xml %{buildroot}%{_datadir}/pear/packages/%{_pearname}.xml

%post
if [ "$1" = "1" ]; then
	if [ -x %{_bindir}/pear -a -f %{_datadir}/pear/packages/%{_pearname}.xml ]; then
		%{_bindir}/pear install --nodeps -r %{_datadir}/pear/packages/%{_pearname}.xml
	fi
fi
if [ "$1" = "2" ]; then
	if [ -x %{_bindir}/pear -a -f %{_datadir}/pear/packages/%{_pearname}.xml ]; then
		%{_bindir}/pear upgrade -f --nodeps -r %{_datadir}/pear/packages/%{_pearname}.xml
	fi
fi

%preun
if [ "$1" = 0 ]; then
	if [ -x %{_bindir}/pear -a -f %{_datadir}/pear/packages/%{_pearname}.xml ]; then
		%{_bindir}/pear uninstall --nodeps -r %{_pearname}
	fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{_pearname}-%{version}/examples
%{_datadir}/pear/%{_class}/*.php
%{_datadir}/pear/packages/%{_pearname}.xml


