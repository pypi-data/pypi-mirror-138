.. cloud_changelog:

==========================
Coiled Cloud Release Notes
==========================

These release notes are related to updates for `cloud.coiled.io <https://cloud.coiled.io>`_.

15 December 2021
================

Fixes
+++++

- Fixed a frontend issue where a pro customer's payment info was not showing up even though it had been entered.
- Fixed an intermittent issue where users for some credit cards were unable to enter their security code. This has
  been fixed and all Credit Cards should work consistently.

Enhancements
++++++++++++

- Dask workers now use public IPs so that NAT Gateway is no longer needed;
  ingress to workers is still blocked. :doc:`tutorials/bring_your_own_network` can disable
  public IPs for workers by setting the the `give_workers_public_ip` option.
- Added a UI for :doc:`bring your own network <tutorials/bring_your_own_network>` so
  network options can also be configured through the UI when selecting your backend.
- Free tier account usage is still on an opt-in model.
  If you are a new user please contact support@coiled.io to enable software
  environments and cluster creations.
- Azure functionality has been removed and disabled for users. Users previously
  hosted on Coiled-hosted Azure have been migrated to the AWS backend.

Documentation
+++++++++++++

- Fixed a couple of broken links in the documentation on teams :doc:`teams`.
- Added more examples to the :doc:`bring your own network <tutorials/bring_your_own_network>`
  documentation.

01 December 2021
================


Enhancements
++++++++++++

- Added ability to manage API access tokens using (optional) expiration dates or
  manual revocation. Added support for managing API tokens via the Coiled Python
  client.
- Added account limit alert when 99% of the quota is used and when your account
  has reached its quota limit.
- Changed the default to use on-demand VMs for Dask workers as opposed to ``spot`` or ``preemptible`` instances.
  Backend options can still be set to use ``spot`` or ``preemptible`` instances, see
  :ref:`AWS backend options<aws_backend_options>` or :ref:`GCP backend options<gcp_backend_options>`.
- Added ability to use pre-existing cloud resources (e.g., VPC, subnets,
  security groups) when running Coiled in your own cloud provider account.

Deprecated
++++++++++

- Coiled Notebooks and Coiled Jobs have been deprecated.


Documentation
+++++++++++++

- As part of upcoming deprecation of the Azure cloud provider backend, the
  documentation related to Azure has been removed.
- Coiled client version of 0.0.55 or higher is required - please update your client if needed.

10 November 2021
================

Fixes
+++++

- Dask workers will now use all CPU/Memory available for the instance type in which they have
  been created. In the past, workers would be limited by your CPU/Memory specification.


Enhancements
++++++++++++

- Moved the **Coiled Subscription** tab up on the account settings page to make it easier
  for you to see how many credits you have used so far.
- If you are using Coiled on your cloud provider, you can now
  customize ingress rules for the firewall/security group created by Coiled
  by specifying ingress ports and a CIDR block.

Deprecated
++++++++++

- Coiled Notebooks and Coiled Jobs were an experimental feature which is being deprecated.
  After December 1, 2021, these will no longer be available.


Documentation
+++++++++++++

- Updated the list of dependencies in the documentation page :doc:`software_environment_creation`
  to include ``dask[complete]`` while creating a software environment with pip.
- Added troubleshooting article for :doc:`repeated cluster timeout errors.
  <troubleshooting/repeated_timeout_errors>`.
- Embedded tutorial videos for :ref:`cluster configuration <cluster-config>`
  and :ref:`software environments <software-envs>` documentation.

27 October 2021
===============

Fixes
+++++

- The route table for the private subnet that is created when Coiled creates a VPC
  in your AWS account, is now called ``coiled-vm-private-router`` instead of
  ``coiled-vm-public-router``.
- Mitigate Rate Limit exceptions when performing some actions like scaling clusters,
  which should improve cluster reliability.
- Software environment names must now be lowercase only.


Enhancements
++++++++++++

- Removed experimental warnings for GCP and Azure in the UI when choosing a
  backend option for an account.
- Removed fallback option to fetch logs from instances via SSH.


Documentation
+++++++++++++

- Removed experimental notes for GCP and Azure in the respective section of
  the documentation for these backends.
- Updated default ``worker_memory`` to ``8GiB`` in a few pages where it was
  saying that the default was ``16GiB``.
- Added a section about network architecture to the :doc:`security` page.
- Added a tutorial on :doc:`tutorials/select_instance_types`.
- Added a tutorial on :doc:`tutorials/select_gpu_type`.
- Added section on selecting instance types in the documentation page
  :doc:`cluster_creation`.
- Added a Networking section on the documentation page for the :doc:`backends_aws`
  that explains how you can specify your AWS security groups using the new arguments
  ``enable_public_http``, ``enable_public_ssh`` and ``disable_public_ingress``.


13 October 2021
===============

Fixes
+++++

* Environment variables sent to the Cluster with the keyword argument
  ``environ=`` are now being converted to strings, which fixes
  occasional failures when sending non-string values to the Cluster.

Enhancements
++++++++++++

* You can now use Coiled in your own GCP account. Please refer to the
  :doc:`backends_gcp` documentation.
* You can now use Coiled in your own Azure account.
* You can now select a ``region`` or ``zone`` when launching clusters in GCP.
* You can now create software environments using Docker images stored in your
  private ECR (AWS), ACR (Azure) or GAR (GCP) container registries, in addition
  to Docker Hub and other registries, by calling
  ``coiled.create_software_environment(container="<URI>")``.
* Coiled now collects statistical profiling data from your Dask clusters.
  This data is visualized as a flame graph on the Analytics page for
  individual clusters.
* You can now hide/show columns in the Clusters Dashboard. The options are: Id,
  Cluster Name, Created By, Status, Num Workers, Software Environment,
  Cost (current), Cost(total), Last Seen, Backend, Runtime, Spot/Preemptible.
* Improve log filtering for AWS when viewing logs in the Coiled UI.


Documentation
+++++++++++++

* Added a new example on using the :doc:`Dask Snowflake <examples/snowflake>`
  connector.
* Fix link to Coiled's privacy policy in the :doc:`security` page.
* Added new section in the :doc:`gpu` documentation to demonstrate the use how
  of GPUs with the Afar library to run remote commands.


28 September 2021
=================

Fixes
+++++

* Resolve error that was throwing an "Unable to stop cluster" error message in the Clusters
  Dashboard for users using the Azure backend.
* Fix issue with workers not being created when users create a new Cluster using the AWS backend.
* Resolve error that was causing Clusters to shut down immediately upon creation for users using the AWS backend.
* Fix issue that was causing the Cluster Dashboard table to show zero workers count even though the workers were
  created and connected to the scheduler.


Enhancements
++++++++++++

* Add label containing the instance name to notification when running ``coiled.get_notifications()``.


Documentation
+++++++++++++

* Fix typo in CLI command, documentation mentioned ``coiled inspect`` but the right command is ``coiled env inspect``.
* Update :doc:`teams` page to better explain the distinction between Accounts and Teams.
