<?php
/* Autoloader for composer/composer and its dependencies */

$vendorDir = '/usr/share/php';
require_once $vendorDir . '/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('Composer\\', __DIR__);

// Dependencies
\Fedora\Autoloader\Dependencies::required([
	$vendorDir . '/Symfony/Component/Console/autoload.php',
	$vendorDir . '/Symfony/Component/Finder/autoload.php',
	$vendorDir . '/Symfony/Component/Process/autoload.php',
	$vendorDir . '/Symfony/Component/Filesystem/autoload.php',
	$vendorDir . '/Seld/JsonLint/autoload.php',
	$vendorDir . '/Seld/PharUtils/autoload.php',
	$vendorDir . '/Seld/CliPrompt/autoload.php',
	$vendorDir . '/Composer/CaBundle/autoload.php',
	$vendorDir . '/Composer/Spdx/autoload.php',
	$vendorDir . '/Composer/Semver/autoload.php',
	$vendorDir . '/Psr/Log/autoload.php',
	$vendorDir . '/JsonSchema5/autoload.php',
]);

