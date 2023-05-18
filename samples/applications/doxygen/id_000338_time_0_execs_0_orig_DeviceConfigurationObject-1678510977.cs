// Copyright (c) Microsoft Corporation.  All Rights Reserved.  Licensed under the MIT License.  See License in the project root for license information.

namespace Microsoft.Intune.PowerShellGraphSDK.PowerShellCmdlets
{
    using System.Management.Automation;

    /// <summary>
    ///     <para type="synopsis">Creates a new object which represents a &quot;microsoft.graph.deviceConfiguration&quot; (or one of its derived types).</para>
    ///     <para type="description">Creates a new object which represents a &quot;microsoft.graph.deviceConfiguration&quot; (or one of its derived types).</para>
    ///     <para type="description">Device Configuration.</para>
    /// </summary>
    [Cmdlet("New", "DeviceConfigurationObject", DefaultParameterSetName = @"microsoft.graph.deviceConfiguration")]
    [ODataType("microsoft.graph.deviceConfiguration")]
    public class New_DeviceConfigurationObject : ObjectFactoryCmdletBase
    {
        /// <summary>
        ///     <para type="description">The &quot;lastModifiedDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.deviceConfiguration&quot; type.</para>
        ///     <para type="description">DateTime the object was last modified.</para>
        /// </summary>
        [ODataType("Edm.DateTimeOffset")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.deviceConfiguration", HelpMessage = @"The &quot;lastModifiedDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10TeamGeneralConfiguration", HelpMessage = @"The &quot;lastModifiedDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", HelpMessage = @"The &quot;lastModifiedDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;lastModifiedDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsUpdateForBusinessConfiguration", HelpMessage = @"The &quot;lastModifiedDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81CustomConfiguration", HelpMessage = @"The &quot;lastModifiedDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10SecureAssessmentConfiguration", HelpMessage = @"The &quot;lastModifiedDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.sharedPCConfiguration", HelpMessage = @"The &quot;lastModifiedDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EnterpriseModernAppManagementConfiguration", HelpMessage = @"The &quot;lastModifiedDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10CustomConfiguration", HelpMessage = @"The &quot;lastModifiedDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.editionUpgradeConfiguration", HelpMessage = @"The &quot;lastModifiedDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsDefenderAdvancedThreatProtectionConfiguration", HelpMessage = @"The &quot;lastModifiedDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;lastModifiedDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;lastModifiedDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.appleDeviceFeaturesConfigurationBase", HelpMessage = @"The &quot;lastModifiedDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSDeviceFeaturesConfiguration", HelpMessage = @"The &quot;lastModifiedDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosDeviceFeaturesConfiguration", HelpMessage = @"The &quot;lastModifiedDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSGeneralDeviceConfiguration", HelpMessage = @"The &quot;lastModifiedDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSCustomConfiguration", HelpMessage = @"The &quot;lastModifiedDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosUpdateConfiguration", HelpMessage = @"The &quot;lastModifiedDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;lastModifiedDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosCustomConfiguration", HelpMessage = @"The &quot;lastModifiedDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosCertificateProfile", HelpMessage = @"The &quot;lastModifiedDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;lastModifiedDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileCustomConfiguration", HelpMessage = @"The &quot;lastModifiedDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;lastModifiedDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidCustomConfiguration", HelpMessage = @"The &quot;lastModifiedDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        public System.DateTimeOffset lastModifiedDateTime { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;createdDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.deviceConfiguration&quot; type.</para>
        ///     <para type="description">DateTime the object was created.</para>
        /// </summary>
        [ODataType("Edm.DateTimeOffset")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.deviceConfiguration", HelpMessage = @"The &quot;createdDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10TeamGeneralConfiguration", HelpMessage = @"The &quot;createdDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", HelpMessage = @"The &quot;createdDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;createdDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsUpdateForBusinessConfiguration", HelpMessage = @"The &quot;createdDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81CustomConfiguration", HelpMessage = @"The &quot;createdDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10SecureAssessmentConfiguration", HelpMessage = @"The &quot;createdDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.sharedPCConfiguration", HelpMessage = @"The &quot;createdDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EnterpriseModernAppManagementConfiguration", HelpMessage = @"The &quot;createdDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10CustomConfiguration", HelpMessage = @"The &quot;createdDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.editionUpgradeConfiguration", HelpMessage = @"The &quot;createdDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsDefenderAdvancedThreatProtectionConfiguration", HelpMessage = @"The &quot;createdDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;createdDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;createdDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.appleDeviceFeaturesConfigurationBase", HelpMessage = @"The &quot;createdDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSDeviceFeaturesConfiguration", HelpMessage = @"The &quot;createdDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosDeviceFeaturesConfiguration", HelpMessage = @"The &quot;createdDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSGeneralDeviceConfiguration", HelpMessage = @"The &quot;createdDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSCustomConfiguration", HelpMessage = @"The &quot;createdDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosUpdateConfiguration", HelpMessage = @"The &quot;createdDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;createdDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosCustomConfiguration", HelpMessage = @"The &quot;createdDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosCertificateProfile", HelpMessage = @"The &quot;createdDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;createdDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileCustomConfiguration", HelpMessage = @"The &quot;createdDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;createdDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidCustomConfiguration", HelpMessage = @"The &quot;createdDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        public System.DateTimeOffset createdDateTime { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;description&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.deviceConfiguration&quot; type.</para>
        ///     <para type="description">Admin provided description of the Device Configuration.</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.deviceConfiguration", HelpMessage = @"The &quot;description&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10TeamGeneralConfiguration", HelpMessage = @"The &quot;description&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", HelpMessage = @"The &quot;description&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;description&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsUpdateForBusinessConfiguration", HelpMessage = @"The &quot;description&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81CustomConfiguration", HelpMessage = @"The &quot;description&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10SecureAssessmentConfiguration", HelpMessage = @"The &quot;description&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.sharedPCConfiguration", HelpMessage = @"The &quot;description&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EnterpriseModernAppManagementConfiguration", HelpMessage = @"The &quot;description&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10CustomConfiguration", HelpMessage = @"The &quot;description&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.editionUpgradeConfiguration", HelpMessage = @"The &quot;description&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsDefenderAdvancedThreatProtectionConfiguration", HelpMessage = @"The &quot;description&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;description&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;description&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.appleDeviceFeaturesConfigurationBase", HelpMessage = @"The &quot;description&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSDeviceFeaturesConfiguration", HelpMessage = @"The &quot;description&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosDeviceFeaturesConfiguration", HelpMessage = @"The &quot;description&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSGeneralDeviceConfiguration", HelpMessage = @"The &quot;description&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSCustomConfiguration", HelpMessage = @"The &quot;description&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosUpdateConfiguration", HelpMessage = @"The &quot;description&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;description&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosCustomConfiguration", HelpMessage = @"The &quot;description&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosCertificateProfile", HelpMessage = @"The &quot;description&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;description&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileCustomConfiguration", HelpMessage = @"The &quot;description&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;description&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidCustomConfiguration", HelpMessage = @"The &quot;description&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String description { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;displayName&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.deviceConfiguration&quot; type.</para>
        ///     <para type="description">Admin provided name of the device configuration.</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.deviceConfiguration", HelpMessage = @"The &quot;displayName&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10TeamGeneralConfiguration", HelpMessage = @"The &quot;displayName&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", HelpMessage = @"The &quot;displayName&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;displayName&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsUpdateForBusinessConfiguration", HelpMessage = @"The &quot;displayName&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81CustomConfiguration", HelpMessage = @"The &quot;displayName&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10SecureAssessmentConfiguration", HelpMessage = @"The &quot;displayName&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.sharedPCConfiguration", HelpMessage = @"The &quot;displayName&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EnterpriseModernAppManagementConfiguration", HelpMessage = @"The &quot;displayName&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10CustomConfiguration", HelpMessage = @"The &quot;displayName&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.editionUpgradeConfiguration", HelpMessage = @"The &quot;displayName&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsDefenderAdvancedThreatProtectionConfiguration", HelpMessage = @"The &quot;displayName&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;displayName&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;displayName&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.appleDeviceFeaturesConfigurationBase", HelpMessage = @"The &quot;displayName&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSDeviceFeaturesConfiguration", HelpMessage = @"The &quot;displayName&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosDeviceFeaturesConfiguration", HelpMessage = @"The &quot;displayName&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSGeneralDeviceConfiguration", HelpMessage = @"The &quot;displayName&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSCustomConfiguration", HelpMessage = @"The &quot;displayName&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosUpdateConfiguration", HelpMessage = @"The &quot;displayName&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;displayName&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosCustomConfiguration", HelpMessage = @"The &quot;displayName&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosCertificateProfile", HelpMessage = @"The &quot;displayName&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;displayName&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileCustomConfiguration", HelpMessage = @"The &quot;displayName&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;displayName&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidCustomConfiguration", HelpMessage = @"The &quot;displayName&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String displayName { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;version&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.deviceConfiguration&quot; type.</para>
        ///     <para type="description">Version of the device configuration.</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.deviceConfiguration", HelpMessage = @"The &quot;version&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10TeamGeneralConfiguration", HelpMessage = @"The &quot;version&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", HelpMessage = @"The &quot;version&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;version&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsUpdateForBusinessConfiguration", HelpMessage = @"The &quot;version&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81CustomConfiguration", HelpMessage = @"The &quot;version&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10SecureAssessmentConfiguration", HelpMessage = @"The &quot;version&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.sharedPCConfiguration", HelpMessage = @"The &quot;version&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EnterpriseModernAppManagementConfiguration", HelpMessage = @"The &quot;version&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10CustomConfiguration", HelpMessage = @"The &quot;version&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.editionUpgradeConfiguration", HelpMessage = @"The &quot;version&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsDefenderAdvancedThreatProtectionConfiguration", HelpMessage = @"The &quot;version&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;version&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;version&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.appleDeviceFeaturesConfigurationBase", HelpMessage = @"The &quot;version&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSDeviceFeaturesConfiguration", HelpMessage = @"The &quot;version&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosDeviceFeaturesConfiguration", HelpMessage = @"The &quot;version&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSGeneralDeviceConfiguration", HelpMessage = @"The &quot;version&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSCustomConfiguration", HelpMessage = @"The &quot;version&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosUpdateConfiguration", HelpMessage = @"The &quot;version&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;version&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosCustomConfiguration", HelpMessage = @"The &quot;version&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosCertificateProfile", HelpMessage = @"The &quot;version&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;version&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileCustomConfiguration", HelpMessage = @"The &quot;version&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;version&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidCustomConfiguration", HelpMessage = @"The &quot;version&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 version { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;assignments&quot; property, of type &quot;microsoft.graph.deviceConfigurationAssignment&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.deviceConfiguration&quot; type.</para>
        ///     <para type="description">The list of assignments for the device configuration profile.</para>
        /// </summary>
        [ODataType("microsoft.graph.deviceConfigurationAssignment")]
        [Selectable]
        [Expandable]
        [AllowEmptyCollection]
        [Parameter(ParameterSetName = @"microsoft.graph.deviceConfiguration", HelpMessage = @"The &quot;assignments&quot; property, of type &quot;microsoft.graph.deviceConfigurationAssignment&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10TeamGeneralConfiguration", HelpMessage = @"The &quot;assignments&quot; property, of type &quot;microsoft.graph.deviceConfigurationAssignment&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", HelpMessage = @"The &quot;assignments&quot; property, of type &quot;microsoft.graph.deviceConfigurationAssignment&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;assignments&quot; property, of type &quot;microsoft.graph.deviceConfigurationAssignment&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsUpdateForBusinessConfiguration", HelpMessage = @"The &quot;assignments&quot; property, of type &quot;microsoft.graph.deviceConfigurationAssignment&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81CustomConfiguration", HelpMessage = @"The &quot;assignments&quot; property, of type &quot;microsoft.graph.deviceConfigurationAssignment&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10SecureAssessmentConfiguration", HelpMessage = @"The &quot;assignments&quot; property, of type &quot;microsoft.graph.deviceConfigurationAssignment&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.sharedPCConfiguration", HelpMessage = @"The &quot;assignments&quot; property, of type &quot;microsoft.graph.deviceConfigurationAssignment&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EnterpriseModernAppManagementConfiguration", HelpMessage = @"The &quot;assignments&quot; property, of type &quot;microsoft.graph.deviceConfigurationAssignment&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10CustomConfiguration", HelpMessage = @"The &quot;assignments&quot; property, of type &quot;microsoft.graph.deviceConfigurationAssignment&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.editionUpgradeConfiguration", HelpMessage = @"The &quot;assignments&quot; property, of type &quot;microsoft.graph.deviceConfigurationAssignment&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsDefenderAdvancedThreatProtectionConfiguration", HelpMessage = @"The &quot;assignments&quot; property, of type &quot;microsoft.graph.deviceConfigurationAssignment&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;assignments&quot; property, of type &quot;microsoft.graph.deviceConfigurationAssignment&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;assignments&quot; property, of type &quot;microsoft.graph.deviceConfigurationAssignment&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.appleDeviceFeaturesConfigurationBase", HelpMessage = @"The &quot;assignments&quot; property, of type &quot;microsoft.graph.deviceConfigurationAssignment&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSDeviceFeaturesConfiguration", HelpMessage = @"The &quot;assignments&quot; property, of type &quot;microsoft.graph.deviceConfigurationAssignment&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosDeviceFeaturesConfiguration", HelpMessage = @"The &quot;assignments&quot; property, of type &quot;microsoft.graph.deviceConfigurationAssignment&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSGeneralDeviceConfiguration", HelpMessage = @"The &quot;assignments&quot; property, of type &quot;microsoft.graph.deviceConfigurationAssignment&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSCustomConfiguration", HelpMessage = @"The &quot;assignments&quot; property, of type &quot;microsoft.graph.deviceConfigurationAssignment&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosUpdateConfiguration", HelpMessage = @"The &quot;assignments&quot; property, of type &quot;microsoft.graph.deviceConfigurationAssignment&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;assignments&quot; property, of type &quot;microsoft.graph.deviceConfigurationAssignment&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosCustomConfiguration", HelpMessage = @"The &quot;assignments&quot; property, of type &quot;microsoft.graph.deviceConfigurationAssignment&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosCertificateProfile", HelpMessage = @"The &quot;assignments&quot; property, of type &quot;microsoft.graph.deviceConfigurationAssignment&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;assignments&quot; property, of type &quot;microsoft.graph.deviceConfigurationAssignment&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileCustomConfiguration", HelpMessage = @"The &quot;assignments&quot; property, of type &quot;microsoft.graph.deviceConfigurationAssignment&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;assignments&quot; property, of type &quot;microsoft.graph.deviceConfigurationAssignment&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidCustomConfiguration", HelpMessage = @"The &quot;assignments&quot; property, of type &quot;microsoft.graph.deviceConfigurationAssignment&quot;.")]
        public System.Object[] assignments { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;deviceStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceStatus&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.deviceConfiguration&quot; type.</para>
        ///     <para type="description">Device configuration installation status by device.</para>
        /// </summary>
        [ODataType("microsoft.graph.deviceConfigurationDeviceStatus")]
        [Selectable]
        [Expandable]
        [AllowEmptyCollection]
        [Parameter(ParameterSetName = @"microsoft.graph.deviceConfiguration", HelpMessage = @"The &quot;deviceStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10TeamGeneralConfiguration", HelpMessage = @"The &quot;deviceStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", HelpMessage = @"The &quot;deviceStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;deviceStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsUpdateForBusinessConfiguration", HelpMessage = @"The &quot;deviceStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81CustomConfiguration", HelpMessage = @"The &quot;deviceStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10SecureAssessmentConfiguration", HelpMessage = @"The &quot;deviceStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.sharedPCConfiguration", HelpMessage = @"The &quot;deviceStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EnterpriseModernAppManagementConfiguration", HelpMessage = @"The &quot;deviceStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10CustomConfiguration", HelpMessage = @"The &quot;deviceStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.editionUpgradeConfiguration", HelpMessage = @"The &quot;deviceStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsDefenderAdvancedThreatProtectionConfiguration", HelpMessage = @"The &quot;deviceStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;deviceStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;deviceStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.appleDeviceFeaturesConfigurationBase", HelpMessage = @"The &quot;deviceStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSDeviceFeaturesConfiguration", HelpMessage = @"The &quot;deviceStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosDeviceFeaturesConfiguration", HelpMessage = @"The &quot;deviceStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSGeneralDeviceConfiguration", HelpMessage = @"The &quot;deviceStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSCustomConfiguration", HelpMessage = @"The &quot;deviceStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosUpdateConfiguration", HelpMessage = @"The &quot;deviceStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;deviceStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosCustomConfiguration", HelpMessage = @"The &quot;deviceStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosCertificateProfile", HelpMessage = @"The &quot;deviceStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;deviceStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileCustomConfiguration", HelpMessage = @"The &quot;deviceStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;deviceStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidCustomConfiguration", HelpMessage = @"The &quot;deviceStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceStatus&quot;.")]
        public System.Object[] deviceStatuses { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;userStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserStatus&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.deviceConfiguration&quot; type.</para>
        ///     <para type="description">Device configuration installation status by user.</para>
        /// </summary>
        [ODataType("microsoft.graph.deviceConfigurationUserStatus")]
        [Selectable]
        [Expandable]
        [AllowEmptyCollection]
        [Parameter(ParameterSetName = @"microsoft.graph.deviceConfiguration", HelpMessage = @"The &quot;userStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10TeamGeneralConfiguration", HelpMessage = @"The &quot;userStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", HelpMessage = @"The &quot;userStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;userStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsUpdateForBusinessConfiguration", HelpMessage = @"The &quot;userStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81CustomConfiguration", HelpMessage = @"The &quot;userStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10SecureAssessmentConfiguration", HelpMessage = @"The &quot;userStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.sharedPCConfiguration", HelpMessage = @"The &quot;userStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EnterpriseModernAppManagementConfiguration", HelpMessage = @"The &quot;userStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10CustomConfiguration", HelpMessage = @"The &quot;userStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.editionUpgradeConfiguration", HelpMessage = @"The &quot;userStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsDefenderAdvancedThreatProtectionConfiguration", HelpMessage = @"The &quot;userStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;userStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;userStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.appleDeviceFeaturesConfigurationBase", HelpMessage = @"The &quot;userStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSDeviceFeaturesConfiguration", HelpMessage = @"The &quot;userStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosDeviceFeaturesConfiguration", HelpMessage = @"The &quot;userStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSGeneralDeviceConfiguration", HelpMessage = @"The &quot;userStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSCustomConfiguration", HelpMessage = @"The &quot;userStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosUpdateConfiguration", HelpMessage = @"The &quot;userStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;userStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosCustomConfiguration", HelpMessage = @"The &quot;userStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosCertificateProfile", HelpMessage = @"The &quot;userStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;userStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileCustomConfiguration", HelpMessage = @"The &quot;userStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;userStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserStatus&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidCustomConfiguration", HelpMessage = @"The &quot;userStatuses&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserStatus&quot;.")]
        public System.Object[] userStatuses { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;deviceStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceOverview&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.deviceConfiguration&quot; type.</para>
        ///     <para type="description">Device Configuration devices status overview</para>
        /// </summary>
        [ODataType("microsoft.graph.deviceConfigurationDeviceOverview")]
        [Selectable]
        [Expandable]
        [Parameter(ParameterSetName = @"microsoft.graph.deviceConfiguration", HelpMessage = @"The &quot;deviceStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10TeamGeneralConfiguration", HelpMessage = @"The &quot;deviceStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", HelpMessage = @"The &quot;deviceStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;deviceStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsUpdateForBusinessConfiguration", HelpMessage = @"The &quot;deviceStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81CustomConfiguration", HelpMessage = @"The &quot;deviceStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10SecureAssessmentConfiguration", HelpMessage = @"The &quot;deviceStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.sharedPCConfiguration", HelpMessage = @"The &quot;deviceStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EnterpriseModernAppManagementConfiguration", HelpMessage = @"The &quot;deviceStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10CustomConfiguration", HelpMessage = @"The &quot;deviceStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.editionUpgradeConfiguration", HelpMessage = @"The &quot;deviceStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsDefenderAdvancedThreatProtectionConfiguration", HelpMessage = @"The &quot;deviceStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;deviceStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;deviceStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.appleDeviceFeaturesConfigurationBase", HelpMessage = @"The &quot;deviceStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSDeviceFeaturesConfiguration", HelpMessage = @"The &quot;deviceStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosDeviceFeaturesConfiguration", HelpMessage = @"The &quot;deviceStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSGeneralDeviceConfiguration", HelpMessage = @"The &quot;deviceStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSCustomConfiguration", HelpMessage = @"The &quot;deviceStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosUpdateConfiguration", HelpMessage = @"The &quot;deviceStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;deviceStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosCustomConfiguration", HelpMessage = @"The &quot;deviceStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosCertificateProfile", HelpMessage = @"The &quot;deviceStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;deviceStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileCustomConfiguration", HelpMessage = @"The &quot;deviceStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;deviceStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidCustomConfiguration", HelpMessage = @"The &quot;deviceStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationDeviceOverview&quot;.")]
        public System.Object deviceStatusOverview { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;userStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserOverview&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.deviceConfiguration&quot; type.</para>
        ///     <para type="description">Device Configuration users status overview</para>
        /// </summary>
        [ODataType("microsoft.graph.deviceConfigurationUserOverview")]
        [Selectable]
        [Expandable]
        [Parameter(ParameterSetName = @"microsoft.graph.deviceConfiguration", HelpMessage = @"The &quot;userStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10TeamGeneralConfiguration", HelpMessage = @"The &quot;userStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", HelpMessage = @"The &quot;userStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;userStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsUpdateForBusinessConfiguration", HelpMessage = @"The &quot;userStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81CustomConfiguration", HelpMessage = @"The &quot;userStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10SecureAssessmentConfiguration", HelpMessage = @"The &quot;userStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.sharedPCConfiguration", HelpMessage = @"The &quot;userStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EnterpriseModernAppManagementConfiguration", HelpMessage = @"The &quot;userStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10CustomConfiguration", HelpMessage = @"The &quot;userStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.editionUpgradeConfiguration", HelpMessage = @"The &quot;userStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsDefenderAdvancedThreatProtectionConfiguration", HelpMessage = @"The &quot;userStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;userStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;userStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.appleDeviceFeaturesConfigurationBase", HelpMessage = @"The &quot;userStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSDeviceFeaturesConfiguration", HelpMessage = @"The &quot;userStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosDeviceFeaturesConfiguration", HelpMessage = @"The &quot;userStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSGeneralDeviceConfiguration", HelpMessage = @"The &quot;userStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSCustomConfiguration", HelpMessage = @"The &quot;userStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosUpdateConfiguration", HelpMessage = @"The &quot;userStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;userStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosCustomConfiguration", HelpMessage = @"The &quot;userStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosCertificateProfile", HelpMessage = @"The &quot;userStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;userStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileCustomConfiguration", HelpMessage = @"The &quot;userStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;userStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserOverview&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidCustomConfiguration", HelpMessage = @"The &quot;userStatusOverview&quot; property, of type &quot;microsoft.graph.deviceConfigurationUserOverview&quot;.")]
        public System.Object userStatusOverview { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;deviceSettingStateSummaries&quot; property, of type &quot;microsoft.graph.settingStateDeviceSummary&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.deviceConfiguration&quot; type.</para>
        ///     <para type="description">Device Configuration Setting State Device Summary</para>
        /// </summary>
        [ODataType("microsoft.graph.settingStateDeviceSummary")]
        [Selectable]
        [Expandable]
        [AllowEmptyCollection]
        [Parameter(ParameterSetName = @"microsoft.graph.deviceConfiguration", HelpMessage = @"The &quot;deviceSettingStateSummaries&quot; property, of type &quot;microsoft.graph.settingStateDeviceSummary&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10TeamGeneralConfiguration", HelpMessage = @"The &quot;deviceSettingStateSummaries&quot; property, of type &quot;microsoft.graph.settingStateDeviceSummary&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", HelpMessage = @"The &quot;deviceSettingStateSummaries&quot; property, of type &quot;microsoft.graph.settingStateDeviceSummary&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;deviceSettingStateSummaries&quot; property, of type &quot;microsoft.graph.settingStateDeviceSummary&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsUpdateForBusinessConfiguration", HelpMessage = @"The &quot;deviceSettingStateSummaries&quot; property, of type &quot;microsoft.graph.settingStateDeviceSummary&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81CustomConfiguration", HelpMessage = @"The &quot;deviceSettingStateSummaries&quot; property, of type &quot;microsoft.graph.settingStateDeviceSummary&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10SecureAssessmentConfiguration", HelpMessage = @"The &quot;deviceSettingStateSummaries&quot; property, of type &quot;microsoft.graph.settingStateDeviceSummary&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.sharedPCConfiguration", HelpMessage = @"The &quot;deviceSettingStateSummaries&quot; property, of type &quot;microsoft.graph.settingStateDeviceSummary&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EnterpriseModernAppManagementConfiguration", HelpMessage = @"The &quot;deviceSettingStateSummaries&quot; property, of type &quot;microsoft.graph.settingStateDeviceSummary&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10CustomConfiguration", HelpMessage = @"The &quot;deviceSettingStateSummaries&quot; property, of type &quot;microsoft.graph.settingStateDeviceSummary&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.editionUpgradeConfiguration", HelpMessage = @"The &quot;deviceSettingStateSummaries&quot; property, of type &quot;microsoft.graph.settingStateDeviceSummary&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsDefenderAdvancedThreatProtectionConfiguration", HelpMessage = @"The &quot;deviceSettingStateSummaries&quot; property, of type &quot;microsoft.graph.settingStateDeviceSummary&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;deviceSettingStateSummaries&quot; property, of type &quot;microsoft.graph.settingStateDeviceSummary&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;deviceSettingStateSummaries&quot; property, of type &quot;microsoft.graph.settingStateDeviceSummary&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.appleDeviceFeaturesConfigurationBase", HelpMessage = @"The &quot;deviceSettingStateSummaries&quot; property, of type &quot;microsoft.graph.settingStateDeviceSummary&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSDeviceFeaturesConfiguration", HelpMessage = @"The &quot;deviceSettingStateSummaries&quot; property, of type &quot;microsoft.graph.settingStateDeviceSummary&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosDeviceFeaturesConfiguration", HelpMessage = @"The &quot;deviceSettingStateSummaries&quot; property, of type &quot;microsoft.graph.settingStateDeviceSummary&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSGeneralDeviceConfiguration", HelpMessage = @"The &quot;deviceSettingStateSummaries&quot; property, of type &quot;microsoft.graph.settingStateDeviceSummary&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSCustomConfiguration", HelpMessage = @"The &quot;deviceSettingStateSummaries&quot; property, of type &quot;microsoft.graph.settingStateDeviceSummary&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosUpdateConfiguration", HelpMessage = @"The &quot;deviceSettingStateSummaries&quot; property, of type &quot;microsoft.graph.settingStateDeviceSummary&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;deviceSettingStateSummaries&quot; property, of type &quot;microsoft.graph.settingStateDeviceSummary&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosCustomConfiguration", HelpMessage = @"The &quot;deviceSettingStateSummaries&quot; property, of type &quot;microsoft.graph.settingStateDeviceSummary&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosCertificateProfile", HelpMessage = @"The &quot;deviceSettingStateSummaries&quot; property, of type &quot;microsoft.graph.settingStateDeviceSummary&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;deviceSettingStateSummaries&quot; property, of type &quot;microsoft.graph.settingStateDeviceSummary&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileCustomConfiguration", HelpMessage = @"The &quot;deviceSettingStateSummaries&quot; property, of type &quot;microsoft.graph.settingStateDeviceSummary&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;deviceSettingStateSummaries&quot; property, of type &quot;microsoft.graph.settingStateDeviceSummary&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidCustomConfiguration", HelpMessage = @"The &quot;deviceSettingStateSummaries&quot; property, of type &quot;microsoft.graph.settingStateDeviceSummary&quot;.")]
        public System.Object[] deviceSettingStateSummaries { get; set; }

        /// <summary>
        ///     <para type="description">A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.windows10TeamGeneralConfiguration&quot; type.</para>
        /// </summary>
        [Selectable]
        [Expandable]
        [ParameterSetSelector(@"microsoft.graph.windows10TeamGeneralConfiguration")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10TeamGeneralConfiguration", Mandatory = true, HelpMessage = @"A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.windows10TeamGeneralConfiguration&quot; type.")]
        public System.Management.Automation.SwitchParameter windows10TeamGeneralConfiguration { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;azureOperationalInsightsBlockTelemetry&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10TeamGeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to Block Azure Operational Insights.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10TeamGeneralConfiguration", HelpMessage = @"The &quot;azureOperationalInsightsBlockTelemetry&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean azureOperationalInsightsBlockTelemetry { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;azureOperationalInsightsWorkspaceId&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10TeamGeneralConfiguration&quot; type.</para>
        ///     <para type="description">The Azure Operational Insights workspace id.</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10TeamGeneralConfiguration", HelpMessage = @"The &quot;azureOperationalInsightsWorkspaceId&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String azureOperationalInsightsWorkspaceId { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;azureOperationalInsightsWorkspaceKey&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10TeamGeneralConfiguration&quot; type.</para>
        ///     <para type="description">The Azure Operational Insights Workspace key.</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10TeamGeneralConfiguration", HelpMessage = @"The &quot;azureOperationalInsightsWorkspaceKey&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String azureOperationalInsightsWorkspaceKey { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;connectAppBlockAutoLaunch&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10TeamGeneralConfiguration&quot; type.</para>
        ///     <para type="description">Specifies whether to automatically launch the Connect app whenever a projection is initiated.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10TeamGeneralConfiguration", HelpMessage = @"The &quot;connectAppBlockAutoLaunch&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean connectAppBlockAutoLaunch { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;maintenanceWindowBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10TeamGeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to Block setting a maintenance window for device updates.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10TeamGeneralConfiguration", HelpMessage = @"The &quot;maintenanceWindowBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean maintenanceWindowBlocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;maintenanceWindowDurationInHours&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10TeamGeneralConfiguration&quot; type.</para>
        ///     <para type="description">Maintenance window duration for device updates. Valid values 0 to 5</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10TeamGeneralConfiguration", HelpMessage = @"The &quot;maintenanceWindowDurationInHours&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 maintenanceWindowDurationInHours { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;maintenanceWindowStartTime&quot; property, of type &quot;Edm.TimeOfDay&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10TeamGeneralConfiguration&quot; type.</para>
        ///     <para type="description">Maintenance window start time for device updates.</para>
        /// </summary>
        [ODataType("Edm.TimeOfDay")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10TeamGeneralConfiguration", HelpMessage = @"The &quot;maintenanceWindowStartTime&quot; property, of type &quot;Edm.TimeOfDay&quot;.")]
        public System.TimeSpan maintenanceWindowStartTime { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;miracastChannel&quot; property, of type &quot;microsoft.graph.miracastChannel&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10TeamGeneralConfiguration&quot; type.</para>
        ///     <para type="description">The channel.</para>
        ///     <para type="description">
        ///          Valid values: &apos;userDefined&apos;, &apos;one&apos;, &apos;two&apos;, &apos;three&apos;, &apos;four&apos;, &apos;five&apos;, &apos;six&apos;, &apos;seven&apos;, &apos;eight&apos;, &apos;nine&apos;, &apos;ten&apos;, &apos;eleven&apos;, &apos;thirtySix&apos;, &apos;forty&apos;, &apos;fortyFour&apos;, &apos;fortyEight&apos;, &apos;oneHundredFortyNine&apos;, &apos;oneHundredFiftyThree&apos;, &apos;oneHundredFiftySeven&apos;, &apos;oneHundredSixtyOne&apos;, &apos;oneHundredSixtyFive&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.miracastChannel")]
        [Selectable]
        [ValidateSet(@"userDefined", @"one", @"two", @"three", @"four", @"five", @"six", @"seven", @"eight", @"nine", @"ten", @"eleven", @"thirtySix", @"forty", @"fortyFour", @"fortyEight", @"oneHundredFortyNine", @"oneHundredFiftyThree", @"oneHundredFiftySeven", @"oneHundredSixtyOne", @"oneHundredSixtyFive")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10TeamGeneralConfiguration", HelpMessage = @"The &quot;miracastChannel&quot; property, of type &quot;microsoft.graph.miracastChannel&quot;.")]
        public System.String miracastChannel { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;miracastBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10TeamGeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to Block wireless projection.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10TeamGeneralConfiguration", HelpMessage = @"The &quot;miracastBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean miracastBlocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;miracastRequirePin&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10TeamGeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to require a pin for wireless projection.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10TeamGeneralConfiguration", HelpMessage = @"The &quot;miracastRequirePin&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean miracastRequirePin { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;settingsBlockMyMeetingsAndFiles&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10TeamGeneralConfiguration&quot; type.</para>
        ///     <para type="description">Specifies whether to disable the &quot;My meetings and files&quot; feature in the Start menu, which shows the signed-in user&apos;s meetings and files from Office 365.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10TeamGeneralConfiguration", HelpMessage = @"The &quot;settingsBlockMyMeetingsAndFiles&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean settingsBlockMyMeetingsAndFiles { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;settingsBlockSessionResume&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10TeamGeneralConfiguration&quot; type.</para>
        ///     <para type="description">Specifies whether to allow the ability to resume a session when the session times out.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10TeamGeneralConfiguration", HelpMessage = @"The &quot;settingsBlockSessionResume&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean settingsBlockSessionResume { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;settingsBlockSigninSuggestions&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10TeamGeneralConfiguration&quot; type.</para>
        ///     <para type="description">Specifies whether to disable auto-populating of the sign-in dialog with invitees from scheduled meetings.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10TeamGeneralConfiguration", HelpMessage = @"The &quot;settingsBlockSigninSuggestions&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean settingsBlockSigninSuggestions { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;settingsDefaultVolume&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10TeamGeneralConfiguration&quot; type.</para>
        ///     <para type="description">Specifies the default volume value for a new session. Permitted values are 0-100. The default is 45. Valid values 0 to 100</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10TeamGeneralConfiguration", HelpMessage = @"The &quot;settingsDefaultVolume&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 settingsDefaultVolume { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;settingsScreenTimeoutInMinutes&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10TeamGeneralConfiguration&quot; type.</para>
        ///     <para type="description">Specifies the number of minutes until the Hub screen turns off.</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10TeamGeneralConfiguration", HelpMessage = @"The &quot;settingsScreenTimeoutInMinutes&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 settingsScreenTimeoutInMinutes { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;settingsSessionTimeoutInMinutes&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10TeamGeneralConfiguration&quot; type.</para>
        ///     <para type="description">Specifies the number of minutes until the session times out.</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10TeamGeneralConfiguration", HelpMessage = @"The &quot;settingsSessionTimeoutInMinutes&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 settingsSessionTimeoutInMinutes { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;settingsSleepTimeoutInMinutes&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10TeamGeneralConfiguration&quot; type.</para>
        ///     <para type="description">Specifies the number of minutes until the Hub enters sleep mode.</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10TeamGeneralConfiguration", HelpMessage = @"The &quot;settingsSleepTimeoutInMinutes&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 settingsSleepTimeoutInMinutes { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;welcomeScreenBlockAutomaticWakeUp&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10TeamGeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to Block the welcome screen from waking up automatically when someone enters the room.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10TeamGeneralConfiguration", HelpMessage = @"The &quot;welcomeScreenBlockAutomaticWakeUp&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean welcomeScreenBlockAutomaticWakeUp { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;welcomeScreenBackgroundImageUrl&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10TeamGeneralConfiguration&quot; type.</para>
        ///     <para type="description">The welcome screen background image URL. The URL must use the HTTPS protocol and return a PNG image.</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10TeamGeneralConfiguration", HelpMessage = @"The &quot;welcomeScreenBackgroundImageUrl&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String welcomeScreenBackgroundImageUrl { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;welcomeScreenMeetingInformation&quot; property, of type &quot;microsoft.graph.welcomeScreenMeetingInformation&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10TeamGeneralConfiguration&quot; type.</para>
        ///     <para type="description">The welcome screen meeting information shown.</para>
        ///     <para type="description">
        ///          Valid values: &apos;userDefined&apos;, &apos;showOrganizerAndTimeOnly&apos;, &apos;showOrganizerAndTimeAndSubject&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.welcomeScreenMeetingInformation")]
        [Selectable]
        [ValidateSet(@"userDefined", @"showOrganizerAndTimeOnly", @"showOrganizerAndTimeAndSubject")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10TeamGeneralConfiguration", HelpMessage = @"The &quot;welcomeScreenMeetingInformation&quot; property, of type &quot;microsoft.graph.welcomeScreenMeetingInformation&quot;.")]
        public System.String welcomeScreenMeetingInformation { get; set; }

        /// <summary>
        ///     <para type="description">A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.windowsPhone81GeneralConfiguration&quot; type.</para>
        /// </summary>
        [Selectable]
        [Expandable]
        [ParameterSetSelector(@"microsoft.graph.windowsPhone81GeneralConfiguration")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", Mandatory = true, HelpMessage = @"A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.windowsPhone81GeneralConfiguration&quot; type.")]
        public System.Management.Automation.SwitchParameter windowsPhone81GeneralConfiguration { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;applyOnlyToWindowsPhone81&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsPhone81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Value indicating whether this policy only applies to Windows Phone 8.1. This property is read-only.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        public System.Boolean applyOnlyToWindowsPhone81 { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;appsBlockCopyPaste&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsPhone81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block copy paste.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", HelpMessage = @"The &quot;appsBlockCopyPaste&quot; property, of type &quot;Edm.Boolean&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;appsBlockCopyPaste&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean appsBlockCopyPaste { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;bluetoothBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsPhone81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block bluetooth.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", HelpMessage = @"The &quot;bluetoothBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;bluetoothBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;bluetoothBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean bluetoothBlocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;cameraBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsPhone81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block camera.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", HelpMessage = @"The &quot;cameraBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;cameraBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;cameraBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;cameraBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean cameraBlocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;cellularBlockWifiTethering&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsPhone81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block Wi-Fi tethering. Has no impact if Wi-Fi is blocked.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", HelpMessage = @"The &quot;cellularBlockWifiTethering&quot; property, of type &quot;Edm.Boolean&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;cellularBlockWifiTethering&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean cellularBlockWifiTethering { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;compliantAppsList&quot; property, of type &quot;microsoft.graph.appListItem&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsPhone81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">List of apps in the compliance (either allow list or block list, controlled by CompliantAppListType). This collection can contain a maximum of 10000 elements.</para>
        /// </summary>
        [ODataType("microsoft.graph.appListItem")]
        [Selectable]
        [AllowEmptyCollection]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", HelpMessage = @"The &quot;compliantAppsList&quot; property, of type &quot;microsoft.graph.appListItem&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSGeneralDeviceConfiguration", HelpMessage = @"The &quot;compliantAppsList&quot; property, of type &quot;microsoft.graph.appListItem&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;compliantAppsList&quot; property, of type &quot;microsoft.graph.appListItem&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;compliantAppsList&quot; property, of type &quot;microsoft.graph.appListItem&quot;.")]
        public System.Object[] compliantAppsList { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;compliantAppListType&quot; property, of type &quot;microsoft.graph.appListType&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsPhone81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">List that is in the AppComplianceList.</para>
        ///     <para type="description">
        ///          Valid values: &apos;none&apos;, &apos;appsInListCompliant&apos;, &apos;appsNotInListCompliant&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.appListType")]
        [Selectable]
        [ValidateSet(@"none", @"appsInListCompliant", @"appsNotInListCompliant")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", HelpMessage = @"The &quot;compliantAppListType&quot; property, of type &quot;microsoft.graph.appListType&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSGeneralDeviceConfiguration", HelpMessage = @"The &quot;compliantAppListType&quot; property, of type &quot;microsoft.graph.appListType&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;compliantAppListType&quot; property, of type &quot;microsoft.graph.appListType&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;compliantAppListType&quot; property, of type &quot;microsoft.graph.appListType&quot;.")]
        public System.String compliantAppListType { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;diagnosticDataBlockSubmission&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsPhone81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block diagnostic data submission.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", HelpMessage = @"The &quot;diagnosticDataBlockSubmission&quot; property, of type &quot;Edm.Boolean&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;diagnosticDataBlockSubmission&quot; property, of type &quot;Edm.Boolean&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;diagnosticDataBlockSubmission&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean diagnosticDataBlockSubmission { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;emailBlockAddingAccounts&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsPhone81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block custom email accounts.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", HelpMessage = @"The &quot;emailBlockAddingAccounts&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean emailBlockAddingAccounts { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;locationServicesBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsPhone81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block location services.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", HelpMessage = @"The &quot;locationServicesBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;locationServicesBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;locationServicesBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean locationServicesBlocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;microsoftAccountBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsPhone81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block using a Microsoft Account.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", HelpMessage = @"The &quot;microsoftAccountBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;microsoftAccountBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean microsoftAccountBlocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;nfcBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsPhone81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block Near-Field Communication.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", HelpMessage = @"The &quot;nfcBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;nfcBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;nfcBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean nfcBlocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;passwordBlockSimple&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsPhone81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block syncing the calendar.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", HelpMessage = @"The &quot;passwordBlockSimple&quot; property, of type &quot;Edm.Boolean&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;passwordBlockSimple&quot; property, of type &quot;Edm.Boolean&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSGeneralDeviceConfiguration", HelpMessage = @"The &quot;passwordBlockSimple&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean passwordBlockSimple { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;passwordExpirationDays&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsPhone81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Number of days before the password expires.</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", HelpMessage = @"The &quot;passwordExpirationDays&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;passwordExpirationDays&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;passwordExpirationDays&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSGeneralDeviceConfiguration", HelpMessage = @"The &quot;passwordExpirationDays&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;passwordExpirationDays&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;passwordExpirationDays&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 passwordExpirationDays { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;passwordMinimumLength&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsPhone81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Minimum length of passwords.</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", HelpMessage = @"The &quot;passwordMinimumLength&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;passwordMinimumLength&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;passwordMinimumLength&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSGeneralDeviceConfiguration", HelpMessage = @"The &quot;passwordMinimumLength&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;passwordMinimumLength&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;passwordMinimumLength&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 passwordMinimumLength { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;passwordMinutesOfInactivityBeforeScreenTimeout&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsPhone81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Minutes of inactivity before screen timeout.</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", HelpMessage = @"The &quot;passwordMinutesOfInactivityBeforeScreenTimeout&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;passwordMinutesOfInactivityBeforeScreenTimeout&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;passwordMinutesOfInactivityBeforeScreenTimeout&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSGeneralDeviceConfiguration", HelpMessage = @"The &quot;passwordMinutesOfInactivityBeforeScreenTimeout&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;passwordMinutesOfInactivityBeforeScreenTimeout&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;passwordMinutesOfInactivityBeforeScreenTimeout&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 passwordMinutesOfInactivityBeforeScreenTimeout { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;passwordMinimumCharacterSetCount&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsPhone81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Number of character sets a password must contain.</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", HelpMessage = @"The &quot;passwordMinimumCharacterSetCount&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;passwordMinimumCharacterSetCount&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;passwordMinimumCharacterSetCount&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSGeneralDeviceConfiguration", HelpMessage = @"The &quot;passwordMinimumCharacterSetCount&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 passwordMinimumCharacterSetCount { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;passwordPreviousPasswordBlockCount&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsPhone81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Number of previous passwords to block. Valid values 0 to 24</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", HelpMessage = @"The &quot;passwordPreviousPasswordBlockCount&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;passwordPreviousPasswordBlockCount&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;passwordPreviousPasswordBlockCount&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSGeneralDeviceConfiguration", HelpMessage = @"The &quot;passwordPreviousPasswordBlockCount&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;passwordPreviousPasswordBlockCount&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;passwordPreviousPasswordBlockCount&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 passwordPreviousPasswordBlockCount { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;passwordSignInFailureCountBeforeFactoryReset&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsPhone81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Number of sign in failures allowed before factory reset.</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", HelpMessage = @"The &quot;passwordSignInFailureCountBeforeFactoryReset&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;passwordSignInFailureCountBeforeFactoryReset&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;passwordSignInFailureCountBeforeFactoryReset&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;passwordSignInFailureCountBeforeFactoryReset&quot; property, of type &quot;Edm.Int32&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;passwordSignInFailureCountBeforeFactoryReset&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 passwordSignInFailureCountBeforeFactoryReset { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;passwordRequiredType&quot; property, of type &quot;microsoft.graph.requiredPasswordType&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsPhone81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Password type that is required.</para>
        ///     <para type="description">
        ///          Valid values: &apos;deviceDefault&apos;, &apos;alphanumeric&apos;, &apos;numeric&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.androidRequiredPasswordType")]
        [Selectable]
        [ValidateSet(@"deviceDefault", @"alphanumeric", @"numeric")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", HelpMessage = @"The &quot;passwordRequiredType&quot; property, of type &quot;microsoft.graph.requiredPasswordType&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;passwordRequiredType&quot; property, of type &quot;microsoft.graph.requiredPasswordType&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;passwordRequiredType&quot; property, of type &quot;microsoft.graph.requiredPasswordType&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSGeneralDeviceConfiguration", HelpMessage = @"The &quot;passwordRequiredType&quot; property, of type &quot;microsoft.graph.requiredPasswordType&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;passwordRequiredType&quot; property, of type &quot;microsoft.graph.requiredPasswordType&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;passwordRequiredType&quot; property, of type &quot;microsoft.graph.requiredPasswordType&quot;.")]
        public System.String passwordRequiredType { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;passwordRequired&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsPhone81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to require a password.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", HelpMessage = @"The &quot;passwordRequired&quot; property, of type &quot;Edm.Boolean&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;passwordRequired&quot; property, of type &quot;Edm.Boolean&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSGeneralDeviceConfiguration", HelpMessage = @"The &quot;passwordRequired&quot; property, of type &quot;Edm.Boolean&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;passwordRequired&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean passwordRequired { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;screenCaptureBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsPhone81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block screenshots.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", HelpMessage = @"The &quot;screenCaptureBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;screenCaptureBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;screenCaptureBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;screenCaptureBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean screenCaptureBlocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;storageBlockRemovableStorage&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsPhone81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block removable storage.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", HelpMessage = @"The &quot;storageBlockRemovableStorage&quot; property, of type &quot;Edm.Boolean&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;storageBlockRemovableStorage&quot; property, of type &quot;Edm.Boolean&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;storageBlockRemovableStorage&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean storageBlockRemovableStorage { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;storageRequireEncryption&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsPhone81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to require encryption.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", HelpMessage = @"The &quot;storageRequireEncryption&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean storageRequireEncryption { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;webBrowserBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsPhone81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the web browser.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", HelpMessage = @"The &quot;webBrowserBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;webBrowserBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean webBrowserBlocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;wifiBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsPhone81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block Wi-Fi.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", HelpMessage = @"The &quot;wifiBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;wifiBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;wifiBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean wifiBlocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;wifiBlockAutomaticConnectHotspots&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsPhone81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block automatically connecting to Wi-Fi hotspots. Has no impact if Wi-Fi is blocked.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", HelpMessage = @"The &quot;wifiBlockAutomaticConnectHotspots&quot; property, of type &quot;Edm.Boolean&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;wifiBlockAutomaticConnectHotspots&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean wifiBlockAutomaticConnectHotspots { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;wifiBlockHotspotReporting&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsPhone81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block Wi-Fi hotspot reporting. Has no impact if Wi-Fi is blocked.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", HelpMessage = @"The &quot;wifiBlockHotspotReporting&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean wifiBlockHotspotReporting { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;windowsStoreBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsPhone81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the Windows Store.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81GeneralConfiguration", HelpMessage = @"The &quot;windowsStoreBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;windowsStoreBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean windowsStoreBlocked { get; set; }

        /// <summary>
        ///     <para type="description">A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.windows81GeneralConfiguration&quot; type.</para>
        /// </summary>
        [Selectable]
        [Expandable]
        [ParameterSetSelector(@"microsoft.graph.windows81GeneralConfiguration")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", Mandatory = true, HelpMessage = @"A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.windows81GeneralConfiguration&quot; type.")]
        public System.Management.Automation.SwitchParameter windows81GeneralConfiguration { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;accountsBlockAddingNonMicrosoftAccountEmail&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to Block the user from adding email accounts to the device that are not associated with a Microsoft account.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;accountsBlockAddingNonMicrosoftAccountEmail&quot; property, of type &quot;Edm.Boolean&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;accountsBlockAddingNonMicrosoftAccountEmail&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean accountsBlockAddingNonMicrosoftAccountEmail { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;applyOnlyToWindows81&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Value indicating whether this policy only applies to Windows 8.1. This property is read-only.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        public System.Boolean applyOnlyToWindows81 { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;browserBlockAutofill&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block auto fill.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;browserBlockAutofill&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean browserBlockAutofill { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;browserBlockAutomaticDetectionOfIntranetSites&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block automatic detection of Intranet sites.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;browserBlockAutomaticDetectionOfIntranetSites&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean browserBlockAutomaticDetectionOfIntranetSites { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;browserBlockEnterpriseModeAccess&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block enterprise mode access.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;browserBlockEnterpriseModeAccess&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean browserBlockEnterpriseModeAccess { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;browserBlockJavaScript&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to Block the user from using JavaScript.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;browserBlockJavaScript&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean browserBlockJavaScript { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;browserBlockPlugins&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block plug-ins.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;browserBlockPlugins&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean browserBlockPlugins { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;browserBlockPopups&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block popups.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;browserBlockPopups&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean browserBlockPopups { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;browserBlockSendingDoNotTrackHeader&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to Block the user from sending the do not track header.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;browserBlockSendingDoNotTrackHeader&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean browserBlockSendingDoNotTrackHeader { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;browserBlockSingleWordEntryOnIntranetSites&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block a single word entry on Intranet sites.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;browserBlockSingleWordEntryOnIntranetSites&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean browserBlockSingleWordEntryOnIntranetSites { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;browserRequireSmartScreen&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to require the user to use the smart screen filter.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;browserRequireSmartScreen&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean browserRequireSmartScreen { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;browserEnterpriseModeSiteListLocation&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">The enterprise mode site list location. Could be a local file, local network or http location.</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;browserEnterpriseModeSiteListLocation&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String browserEnterpriseModeSiteListLocation { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;browserInternetSecurityLevel&quot; property, of type &quot;microsoft.graph.internetSiteSecurityLevel&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">The internet security level.</para>
        ///     <para type="description">
        ///          Valid values: &apos;userDefined&apos;, &apos;medium&apos;, &apos;mediumHigh&apos;, &apos;high&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.internetSiteSecurityLevel")]
        [Selectable]
        [ValidateSet(@"userDefined", @"medium", @"mediumHigh", @"high")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;browserInternetSecurityLevel&quot; property, of type &quot;microsoft.graph.internetSiteSecurityLevel&quot;.")]
        public System.String browserInternetSecurityLevel { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;browserIntranetSecurityLevel&quot; property, of type &quot;microsoft.graph.siteSecurityLevel&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">The Intranet security level.</para>
        ///     <para type="description">
        ///          Valid values: &apos;userDefined&apos;, &apos;low&apos;, &apos;mediumLow&apos;, &apos;medium&apos;, &apos;mediumHigh&apos;, &apos;high&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.siteSecurityLevel")]
        [Selectable]
        [ValidateSet(@"userDefined", @"low", @"mediumLow", @"medium", @"mediumHigh", @"high")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;browserIntranetSecurityLevel&quot; property, of type &quot;microsoft.graph.siteSecurityLevel&quot;.")]
        public System.String browserIntranetSecurityLevel { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;browserLoggingReportLocation&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">The logging report location.</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;browserLoggingReportLocation&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String browserLoggingReportLocation { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;browserRequireHighSecurityForRestrictedSites&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to require high security for restricted sites.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;browserRequireHighSecurityForRestrictedSites&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean browserRequireHighSecurityForRestrictedSites { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;browserRequireFirewall&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to require a firewall.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;browserRequireFirewall&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean browserRequireFirewall { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;browserRequireFraudWarning&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to require fraud warning.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;browserRequireFraudWarning&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean browserRequireFraudWarning { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;browserTrustedSitesSecurityLevel&quot; property, of type &quot;microsoft.graph.siteSecurityLevel&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">The trusted sites security level.</para>
        ///     <para type="description">
        ///          Valid values: &apos;userDefined&apos;, &apos;low&apos;, &apos;mediumLow&apos;, &apos;medium&apos;, &apos;mediumHigh&apos;, &apos;high&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.siteSecurityLevel")]
        [Selectable]
        [ValidateSet(@"userDefined", @"low", @"mediumLow", @"medium", @"mediumHigh", @"high")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;browserTrustedSitesSecurityLevel&quot; property, of type &quot;microsoft.graph.siteSecurityLevel&quot;.")]
        public System.String browserTrustedSitesSecurityLevel { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;cellularBlockDataRoaming&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block data roaming.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;cellularBlockDataRoaming&quot; property, of type &quot;Edm.Boolean&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;cellularBlockDataRoaming&quot; property, of type &quot;Edm.Boolean&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;cellularBlockDataRoaming&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean cellularBlockDataRoaming { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;diagnosticsBlockDataSubmission&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block diagnostic data submission.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;diagnosticsBlockDataSubmission&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean diagnosticsBlockDataSubmission { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;passwordBlockPicturePasswordAndPin&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to Block the user from using a pictures password and pin.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;passwordBlockPicturePasswordAndPin&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean passwordBlockPicturePasswordAndPin { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;storageRequireDeviceEncryption&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to require encryption on a mobile device.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;storageRequireDeviceEncryption&quot; property, of type &quot;Edm.Boolean&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;storageRequireDeviceEncryption&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean storageRequireDeviceEncryption { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;updatesRequireAutomaticUpdates&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to require automatic updates.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;updatesRequireAutomaticUpdates&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean updatesRequireAutomaticUpdates { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;userAccountControlSettings&quot; property, of type &quot;microsoft.graph.windowsUserAccountControlSettings&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">The user account control settings.</para>
        ///     <para type="description">
        ///          Valid values: &apos;userDefined&apos;, &apos;alwaysNotify&apos;, &apos;notifyOnAppChanges&apos;, &apos;notifyOnAppChangesWithoutDimming&apos;, &apos;neverNotify&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.windowsUserAccountControlSettings")]
        [Selectable]
        [ValidateSet(@"userDefined", @"alwaysNotify", @"notifyOnAppChanges", @"notifyOnAppChangesWithoutDimming", @"neverNotify")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;userAccountControlSettings&quot; property, of type &quot;microsoft.graph.windowsUserAccountControlSettings&quot;.")]
        public System.String userAccountControlSettings { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;workFoldersUrl&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows81GeneralConfiguration&quot; type.</para>
        ///     <para type="description">The work folders url.</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows81GeneralConfiguration", HelpMessage = @"The &quot;workFoldersUrl&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String workFoldersUrl { get; set; }

        /// <summary>
        ///     <para type="description">A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.windowsUpdateForBusinessConfiguration&quot; type.</para>
        /// </summary>
        [Selectable]
        [Expandable]
        [ParameterSetSelector(@"microsoft.graph.windowsUpdateForBusinessConfiguration")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsUpdateForBusinessConfiguration", Mandatory = true, HelpMessage = @"A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.windowsUpdateForBusinessConfiguration&quot; type.")]
        public System.Management.Automation.SwitchParameter windowsUpdateForBusinessConfiguration { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;deliveryOptimizationMode&quot; property, of type &quot;microsoft.graph.windowsDeliveryOptimizationMode&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsUpdateForBusinessConfiguration&quot; type.</para>
        ///     <para type="description">Delivery Optimization Mode</para>
        ///     <para type="description">
        ///          Valid values: &apos;userDefined&apos;, &apos;httpOnly&apos;, &apos;httpWithPeeringNat&apos;, &apos;httpWithPeeringPrivateGroup&apos;, &apos;httpWithInternetPeering&apos;, &apos;simpleDownload&apos;, &apos;bypassMode&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.windowsDeliveryOptimizationMode")]
        [Selectable]
        [ValidateSet(@"userDefined", @"httpOnly", @"httpWithPeeringNat", @"httpWithPeeringPrivateGroup", @"httpWithInternetPeering", @"simpleDownload", @"bypassMode")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsUpdateForBusinessConfiguration", HelpMessage = @"The &quot;deliveryOptimizationMode&quot; property, of type &quot;microsoft.graph.windowsDeliveryOptimizationMode&quot;.")]
        public System.String deliveryOptimizationMode { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;prereleaseFeatures&quot; property, of type &quot;microsoft.graph.prereleaseFeatures&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsUpdateForBusinessConfiguration&quot; type.</para>
        ///     <para type="description">The pre-release features.</para>
        ///     <para type="description">
        ///          Valid values: &apos;userDefined&apos;, &apos;settingsOnly&apos;, &apos;settingsAndExperimentations&apos;, &apos;notAllowed&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.prereleaseFeatures")]
        [Selectable]
        [ValidateSet(@"userDefined", @"settingsOnly", @"settingsAndExperimentations", @"notAllowed")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsUpdateForBusinessConfiguration", HelpMessage = @"The &quot;prereleaseFeatures&quot; property, of type &quot;microsoft.graph.prereleaseFeatures&quot;.")]
        public System.String prereleaseFeatures { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;automaticUpdateMode&quot; property, of type &quot;microsoft.graph.automaticUpdateMode&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsUpdateForBusinessConfiguration&quot; type.</para>
        ///     <para type="description">Automatic update mode.</para>
        ///     <para type="description">
        ///          Valid values: &apos;userDefined&apos;, &apos;notifyDownload&apos;, &apos;autoInstallAtMaintenanceTime&apos;, &apos;autoInstallAndRebootAtMaintenanceTime&apos;, &apos;autoInstallAndRebootAtScheduledTime&apos;, &apos;autoInstallAndRebootWithoutEndUserControl&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.automaticUpdateMode")]
        [Selectable]
        [ValidateSet(@"userDefined", @"notifyDownload", @"autoInstallAtMaintenanceTime", @"autoInstallAndRebootAtMaintenanceTime", @"autoInstallAndRebootAtScheduledTime", @"autoInstallAndRebootWithoutEndUserControl")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsUpdateForBusinessConfiguration", HelpMessage = @"The &quot;automaticUpdateMode&quot; property, of type &quot;microsoft.graph.automaticUpdateMode&quot;.")]
        public System.String automaticUpdateMode { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;microsoftUpdateServiceAllowed&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsUpdateForBusinessConfiguration&quot; type.</para>
        ///     <para type="description">Allow Microsoft Update Service</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsUpdateForBusinessConfiguration", HelpMessage = @"The &quot;microsoftUpdateServiceAllowed&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean microsoftUpdateServiceAllowed { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;driversExcluded&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsUpdateForBusinessConfiguration&quot; type.</para>
        ///     <para type="description">Exclude Windows update Drivers</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsUpdateForBusinessConfiguration", HelpMessage = @"The &quot;driversExcluded&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean driversExcluded { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;installationSchedule&quot; property, of type &quot;microsoft.graph.windowsUpdateInstallScheduleType&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsUpdateForBusinessConfiguration&quot; type.</para>
        ///     <para type="description">Installation schedule</para>
        /// </summary>
        [ODataType("microsoft.graph.windowsUpdateInstallScheduleType", "microsoft.graph.windowsUpdateActiveHoursInstall", "microsoft.graph.windowsUpdateScheduledInstall")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsUpdateForBusinessConfiguration", HelpMessage = @"The &quot;installationSchedule&quot; property, of type &quot;microsoft.graph.windowsUpdateInstallScheduleType&quot;.")]
        public System.Object installationSchedule { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;qualityUpdatesDeferralPeriodInDays&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsUpdateForBusinessConfiguration&quot; type.</para>
        ///     <para type="description">Defer Quality Updates by these many days</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsUpdateForBusinessConfiguration", HelpMessage = @"The &quot;qualityUpdatesDeferralPeriodInDays&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 qualityUpdatesDeferralPeriodInDays { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;featureUpdatesDeferralPeriodInDays&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsUpdateForBusinessConfiguration&quot; type.</para>
        ///     <para type="description">Defer Feature Updates by these many days</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsUpdateForBusinessConfiguration", HelpMessage = @"The &quot;featureUpdatesDeferralPeriodInDays&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 featureUpdatesDeferralPeriodInDays { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;qualityUpdatesPaused&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsUpdateForBusinessConfiguration&quot; type.</para>
        ///     <para type="description">Pause Quality Updates</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsUpdateForBusinessConfiguration", HelpMessage = @"The &quot;qualityUpdatesPaused&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean qualityUpdatesPaused { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;featureUpdatesPaused&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsUpdateForBusinessConfiguration&quot; type.</para>
        ///     <para type="description">Pause Feature Updates</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsUpdateForBusinessConfiguration", HelpMessage = @"The &quot;featureUpdatesPaused&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean featureUpdatesPaused { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;qualityUpdatesPauseExpiryDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsUpdateForBusinessConfiguration&quot; type.</para>
        ///     <para type="description">Quality Updates Pause Expiry datetime</para>
        /// </summary>
        [ODataType("Edm.DateTimeOffset")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsUpdateForBusinessConfiguration", HelpMessage = @"The &quot;qualityUpdatesPauseExpiryDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        public System.DateTimeOffset qualityUpdatesPauseExpiryDateTime { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;featureUpdatesPauseExpiryDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsUpdateForBusinessConfiguration&quot; type.</para>
        ///     <para type="description">Feature Updates Pause Expiry datetime</para>
        /// </summary>
        [ODataType("Edm.DateTimeOffset")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsUpdateForBusinessConfiguration", HelpMessage = @"The &quot;featureUpdatesPauseExpiryDateTime&quot; property, of type &quot;Edm.DateTimeOffset&quot;.")]
        public System.DateTimeOffset featureUpdatesPauseExpiryDateTime { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;businessReadyUpdatesOnly&quot; property, of type &quot;microsoft.graph.windowsUpdateType&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsUpdateForBusinessConfiguration&quot; type.</para>
        ///     <para type="description">Determines which branch devices will receive their updates from</para>
        ///     <para type="description">
        ///          Valid values: &apos;userDefined&apos;, &apos;all&apos;, &apos;businessReadyOnly&apos;, &apos;windowsInsiderBuildFast&apos;, &apos;windowsInsiderBuildSlow&apos;, &apos;windowsInsiderBuildRelease&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.windowsUpdateType")]
        [Selectable]
        [ValidateSet(@"userDefined", @"all", @"businessReadyOnly", @"windowsInsiderBuildFast", @"windowsInsiderBuildSlow", @"windowsInsiderBuildRelease")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsUpdateForBusinessConfiguration", HelpMessage = @"The &quot;businessReadyUpdatesOnly&quot; property, of type &quot;microsoft.graph.windowsUpdateType&quot;.")]
        public System.String businessReadyUpdatesOnly { get; set; }

        /// <summary>
        ///     <para type="description">A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.windowsPhone81CustomConfiguration&quot; type.</para>
        /// </summary>
        [Selectable]
        [Expandable]
        [ParameterSetSelector(@"microsoft.graph.windowsPhone81CustomConfiguration")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81CustomConfiguration", Mandatory = true, HelpMessage = @"A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.windowsPhone81CustomConfiguration&quot; type.")]
        public System.Management.Automation.SwitchParameter windowsPhone81CustomConfiguration { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;omaSettings&quot; property, of type &quot;microsoft.graph.omaSetting&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsPhone81CustomConfiguration&quot; type.</para>
        ///     <para type="description">OMA settings. This collection can contain a maximum of 1000 elements.</para>
        /// </summary>
        [ODataType("microsoft.graph.omaSetting", "microsoft.graph.omaSettingBase64", "microsoft.graph.omaSettingBoolean", "microsoft.graph.omaSettingStringXml", "microsoft.graph.omaSettingDateTime", "microsoft.graph.omaSettingString", "microsoft.graph.omaSettingFloatingPoint", "microsoft.graph.omaSettingInteger")]
        [Selectable]
        [AllowEmptyCollection]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsPhone81CustomConfiguration", HelpMessage = @"The &quot;omaSettings&quot; property, of type &quot;microsoft.graph.omaSetting&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10CustomConfiguration", HelpMessage = @"The &quot;omaSettings&quot; property, of type &quot;microsoft.graph.omaSetting&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileCustomConfiguration", HelpMessage = @"The &quot;omaSettings&quot; property, of type &quot;microsoft.graph.omaSetting&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidCustomConfiguration", HelpMessage = @"The &quot;omaSettings&quot; property, of type &quot;microsoft.graph.omaSetting&quot;.")]
        public System.Object[] omaSettings { get; set; }

        /// <summary>
        ///     <para type="description">A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.windows10SecureAssessmentConfiguration&quot; type.</para>
        /// </summary>
        [Selectable]
        [Expandable]
        [ParameterSetSelector(@"microsoft.graph.windows10SecureAssessmentConfiguration")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10SecureAssessmentConfiguration", Mandatory = true, HelpMessage = @"A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.windows10SecureAssessmentConfiguration&quot; type.")]
        public System.Management.Automation.SwitchParameter windows10SecureAssessmentConfiguration { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;launchUri&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10SecureAssessmentConfiguration&quot; type.</para>
        ///     <para type="description">Url link to an assessment that&apos;s automatically loaded when the secure assessment browser is launched. It has to be a valid Url (http[s]://msdn.microsoft.com/).</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10SecureAssessmentConfiguration", HelpMessage = @"The &quot;launchUri&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String launchUri { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;configurationAccount&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10SecureAssessmentConfiguration&quot; type.</para>
        ///     <para type="description">The account used to configure the Windows device for taking the test. The user can be a domain account (domain\user), an AAD account (username@tenant.com) or a local account (username).</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10SecureAssessmentConfiguration", HelpMessage = @"The &quot;configurationAccount&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String configurationAccount { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;allowPrinting&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10SecureAssessmentConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to allow the app from printing during the test.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10SecureAssessmentConfiguration", HelpMessage = @"The &quot;allowPrinting&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean allowPrinting { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;allowScreenCapture&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10SecureAssessmentConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to allow screen capture capability during a test.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10SecureAssessmentConfiguration", HelpMessage = @"The &quot;allowScreenCapture&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean allowScreenCapture { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;allowTextSuggestion&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10SecureAssessmentConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to allow text suggestions during the test.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10SecureAssessmentConfiguration", HelpMessage = @"The &quot;allowTextSuggestion&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean allowTextSuggestion { get; set; }

        /// <summary>
        ///     <para type="description">A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.sharedPCConfiguration&quot; type.</para>
        /// </summary>
        [Selectable]
        [Expandable]
        [ParameterSetSelector(@"microsoft.graph.sharedPCConfiguration")]
        [Parameter(ParameterSetName = @"microsoft.graph.sharedPCConfiguration", Mandatory = true, HelpMessage = @"A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.sharedPCConfiguration&quot; type.")]
        public System.Management.Automation.SwitchParameter sharedPCConfiguration { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;accountManagerPolicy&quot; property, of type &quot;microsoft.graph.sharedPCAccountManagerPolicy&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.sharedPCConfiguration&quot; type.</para>
        ///     <para type="description">Specifies how accounts are managed on a shared PC. Only applies when disableAccountManager is false.</para>
        /// </summary>
        [ODataType("microsoft.graph.sharedPCAccountManagerPolicy")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.sharedPCConfiguration", HelpMessage = @"The &quot;accountManagerPolicy&quot; property, of type &quot;microsoft.graph.sharedPCAccountManagerPolicy&quot;.")]
        public System.Object accountManagerPolicy { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;allowedAccounts&quot; property, of type &quot;microsoft.graph.sharedPCAllowedAccountType&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.sharedPCConfiguration&quot; type.</para>
        ///     <para type="description">Indicates which type of accounts are allowed to use on a shared PC.</para>
        ///     <para type="description">
        ///          Valid values: &apos;guest&apos;, &apos;domain&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.sharedPCAllowedAccountType")]
        [Selectable]
        [ValidateSet(@"guest", @"domain")]
        [Parameter(ParameterSetName = @"microsoft.graph.sharedPCConfiguration", HelpMessage = @"The &quot;allowedAccounts&quot; property, of type &quot;microsoft.graph.sharedPCAllowedAccountType&quot;.")]
        public System.String allowedAccounts { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;allowLocalStorage&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.sharedPCConfiguration&quot; type.</para>
        ///     <para type="description">Specifies whether local storage is allowed on a shared PC.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.sharedPCConfiguration", HelpMessage = @"The &quot;allowLocalStorage&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean allowLocalStorage { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;disableAccountManager&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.sharedPCConfiguration&quot; type.</para>
        ///     <para type="description">Disables the account manager for shared PC mode.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.sharedPCConfiguration", HelpMessage = @"The &quot;disableAccountManager&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean disableAccountManager { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;disableEduPolicies&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.sharedPCConfiguration&quot; type.</para>
        ///     <para type="description">Specifies whether the default shared PC education environment policies should be disabled. For Windows 10 RS2 and later, this policy will be applied without setting Enabled to true.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.sharedPCConfiguration", HelpMessage = @"The &quot;disableEduPolicies&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean disableEduPolicies { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;disablePowerPolicies&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.sharedPCConfiguration&quot; type.</para>
        ///     <para type="description">Specifies whether the default shared PC power policies should be disabled.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.sharedPCConfiguration", HelpMessage = @"The &quot;disablePowerPolicies&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean disablePowerPolicies { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;disableSignInOnResume&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.sharedPCConfiguration&quot; type.</para>
        ///     <para type="description">Disables the requirement to sign in whenever the device wakes up from sleep mode.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.sharedPCConfiguration", HelpMessage = @"The &quot;disableSignInOnResume&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean disableSignInOnResume { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;enabled&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.sharedPCConfiguration&quot; type.</para>
        ///     <para type="description">Enables shared PC mode and applies the shared pc policies.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.sharedPCConfiguration", HelpMessage = @"The &quot;enabled&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean enabled { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;idleTimeBeforeSleepInSeconds&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.sharedPCConfiguration&quot; type.</para>
        ///     <para type="description">Specifies the time in seconds that a device must sit idle before the PC goes to sleep. Setting this value to 0 prevents the sleep timeout from occurring.</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.sharedPCConfiguration", HelpMessage = @"The &quot;idleTimeBeforeSleepInSeconds&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 idleTimeBeforeSleepInSeconds { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;kioskAppDisplayName&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.sharedPCConfiguration&quot; type.</para>
        ///     <para type="description">Specifies the display text for the account shown on the sign-in screen which launches the app specified by SetKioskAppUserModelId. Only applies when KioskAppUserModelId is set.</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.sharedPCConfiguration", HelpMessage = @"The &quot;kioskAppDisplayName&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String kioskAppDisplayName { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;kioskAppUserModelId&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.sharedPCConfiguration&quot; type.</para>
        ///     <para type="description">Specifies the application user model ID of the app to use with assigned access.</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.sharedPCConfiguration", HelpMessage = @"The &quot;kioskAppUserModelId&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String kioskAppUserModelId { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;maintenanceStartTime&quot; property, of type &quot;Edm.TimeOfDay&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.sharedPCConfiguration&quot; type.</para>
        ///     <para type="description">Specifies the daily start time of maintenance hour.</para>
        /// </summary>
        [ODataType("Edm.TimeOfDay")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.sharedPCConfiguration", HelpMessage = @"The &quot;maintenanceStartTime&quot; property, of type &quot;Edm.TimeOfDay&quot;.")]
        public System.TimeSpan maintenanceStartTime { get; set; }

        /// <summary>
        ///     <para type="description">A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.windows10EnterpriseModernAppManagementConfiguration&quot; type.</para>
        /// </summary>
        [Selectable]
        [Expandable]
        [ParameterSetSelector(@"microsoft.graph.windows10EnterpriseModernAppManagementConfiguration")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EnterpriseModernAppManagementConfiguration", Mandatory = true, HelpMessage = @"A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.windows10EnterpriseModernAppManagementConfiguration&quot; type.")]
        public System.Management.Automation.SwitchParameter windows10EnterpriseModernAppManagementConfiguration { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;uninstallBuiltInApps&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10EnterpriseModernAppManagementConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to uninstall a fixed list of built-in Windows apps.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EnterpriseModernAppManagementConfiguration", HelpMessage = @"The &quot;uninstallBuiltInApps&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean uninstallBuiltInApps { get; set; }

        /// <summary>
        ///     <para type="description">A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.windows10CustomConfiguration&quot; type.</para>
        /// </summary>
        [Selectable]
        [Expandable]
        [ParameterSetSelector(@"microsoft.graph.windows10CustomConfiguration")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10CustomConfiguration", Mandatory = true, HelpMessage = @"A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.windows10CustomConfiguration&quot; type.")]
        public System.Management.Automation.SwitchParameter windows10CustomConfiguration { get; set; }

        /// <summary>
        ///     <para type="description">A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.editionUpgradeConfiguration&quot; type.</para>
        /// </summary>
        [Selectable]
        [Expandable]
        [ParameterSetSelector(@"microsoft.graph.editionUpgradeConfiguration")]
        [Parameter(ParameterSetName = @"microsoft.graph.editionUpgradeConfiguration", Mandatory = true, HelpMessage = @"A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.editionUpgradeConfiguration&quot; type.")]
        public System.Management.Automation.SwitchParameter editionUpgradeConfiguration { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;licenseType&quot; property, of type &quot;microsoft.graph.editionUpgradeLicenseType&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.editionUpgradeConfiguration&quot; type.</para>
        ///     <para type="description">Edition Upgrade License Type.</para>
        ///     <para type="description">
        ///          Valid values: &apos;productKey&apos;, &apos;licenseFile&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.editionUpgradeLicenseType")]
        [Selectable]
        [ValidateSet(@"productKey", @"licenseFile")]
        [Parameter(ParameterSetName = @"microsoft.graph.editionUpgradeConfiguration", HelpMessage = @"The &quot;licenseType&quot; property, of type &quot;microsoft.graph.editionUpgradeLicenseType&quot;.")]
        public System.String licenseType { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;targetEdition&quot; property, of type &quot;microsoft.graph.windows10EditionType&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.editionUpgradeConfiguration&quot; type.</para>
        ///     <para type="description">Edition Upgrade Target Edition.</para>
        ///     <para type="description">
        ///          Valid values: &apos;windows10Enterprise&apos;, &apos;windows10EnterpriseN&apos;, &apos;windows10Education&apos;, &apos;windows10EducationN&apos;, &apos;windows10MobileEnterprise&apos;, &apos;windows10HolographicEnterprise&apos;, &apos;windows10Professional&apos;, &apos;windows10ProfessionalN&apos;, &apos;windows10ProfessionalEducation&apos;, &apos;windows10ProfessionalEducationN&apos;, &apos;windows10ProfessionalWorkstation&apos;, &apos;windows10ProfessionalWorkstationN&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.windows10EditionType")]
        [Selectable]
        [ValidateSet(@"windows10Enterprise", @"windows10EnterpriseN", @"windows10Education", @"windows10EducationN", @"windows10MobileEnterprise", @"windows10HolographicEnterprise", @"windows10Professional", @"windows10ProfessionalN", @"windows10ProfessionalEducation", @"windows10ProfessionalEducationN", @"windows10ProfessionalWorkstation", @"windows10ProfessionalWorkstationN")]
        [Parameter(ParameterSetName = @"microsoft.graph.editionUpgradeConfiguration", HelpMessage = @"The &quot;targetEdition&quot; property, of type &quot;microsoft.graph.windows10EditionType&quot;.")]
        public System.String targetEdition { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;license&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.editionUpgradeConfiguration&quot; type.</para>
        ///     <para type="description">Edition Upgrade License File Content.</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.editionUpgradeConfiguration", HelpMessage = @"The &quot;license&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String license { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;productKey&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.editionUpgradeConfiguration&quot; type.</para>
        ///     <para type="description">Edition Upgrade Product Key.</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.editionUpgradeConfiguration", HelpMessage = @"The &quot;productKey&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String productKey { get; set; }

        /// <summary>
        ///     <para type="description">A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.windowsDefenderAdvancedThreatProtectionConfiguration&quot; type.</para>
        /// </summary>
        [Selectable]
        [Expandable]
        [ParameterSetSelector(@"microsoft.graph.windowsDefenderAdvancedThreatProtectionConfiguration")]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsDefenderAdvancedThreatProtectionConfiguration", Mandatory = true, HelpMessage = @"A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.windowsDefenderAdvancedThreatProtectionConfiguration&quot; type.")]
        public System.Management.Automation.SwitchParameter windowsDefenderAdvancedThreatProtectionConfiguration { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;allowSampleSharing&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsDefenderAdvancedThreatProtectionConfiguration&quot; type.</para>
        ///     <para type="description">Windows Defender AdvancedThreatProtection &quot;Allow Sample Sharing&quot; Rule</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsDefenderAdvancedThreatProtectionConfiguration", HelpMessage = @"The &quot;allowSampleSharing&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean allowSampleSharing { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;enableExpeditedTelemetryReporting&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windowsDefenderAdvancedThreatProtectionConfiguration&quot; type.</para>
        ///     <para type="description">Expedite Windows Defender Advanced Threat Protection telemetry reporting frequency.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windowsDefenderAdvancedThreatProtectionConfiguration", HelpMessage = @"The &quot;enableExpeditedTelemetryReporting&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean enableExpeditedTelemetryReporting { get; set; }

        /// <summary>
        ///     <para type="description">A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        /// </summary>
        [Selectable]
        [Expandable]
        [ParameterSetSelector(@"microsoft.graph.windows10GeneralConfiguration")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", Mandatory = true, HelpMessage = @"A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.")]
        public System.Management.Automation.SwitchParameter windows10GeneralConfiguration { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;enterpriseCloudPrintDiscoveryEndPoint&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Endpoint for discovering cloud printers.</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;enterpriseCloudPrintDiscoveryEndPoint&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String enterpriseCloudPrintDiscoveryEndPoint { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;enterpriseCloudPrintOAuthAuthority&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Authentication endpoint for acquiring OAuth tokens.</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;enterpriseCloudPrintOAuthAuthority&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String enterpriseCloudPrintOAuthAuthority { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;enterpriseCloudPrintOAuthClientIdentifier&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">GUID of a client application authorized to retrieve OAuth tokens from the OAuth Authority.</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;enterpriseCloudPrintOAuthClientIdentifier&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String enterpriseCloudPrintOAuthClientIdentifier { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;enterpriseCloudPrintResourceIdentifier&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">OAuth resource URI for print service as configured in the Azure portal.</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;enterpriseCloudPrintResourceIdentifier&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String enterpriseCloudPrintResourceIdentifier { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;enterpriseCloudPrintDiscoveryMaxLimit&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Maximum number of printers that should be queried from a discovery endpoint. This is a mobile only setting. Valid values 1 to 65535</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;enterpriseCloudPrintDiscoveryMaxLimit&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 enterpriseCloudPrintDiscoveryMaxLimit { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;enterpriseCloudPrintMopriaDiscoveryResourceIdentifier&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">OAuth resource URI for printer discovery service as configured in Azure portal.</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;enterpriseCloudPrintMopriaDiscoveryResourceIdentifier&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String enterpriseCloudPrintMopriaDiscoveryResourceIdentifier { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;searchBlockDiacritics&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Specifies if search can use diacritics.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;searchBlockDiacritics&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean searchBlockDiacritics { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;searchDisableAutoLanguageDetection&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Specifies whether to use automatic language detection when indexing content and properties.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;searchDisableAutoLanguageDetection&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean searchDisableAutoLanguageDetection { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;searchDisableIndexingEncryptedItems&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block indexing of WIP-protected items to prevent them from appearing in search results for Cortana or Explorer.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;searchDisableIndexingEncryptedItems&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean searchDisableIndexingEncryptedItems { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;searchEnableRemoteQueries&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block remote queries of this computer’s index.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;searchEnableRemoteQueries&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean searchEnableRemoteQueries { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;searchDisableIndexerBackoff&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to disable the search indexer backoff feature.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;searchDisableIndexerBackoff&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean searchDisableIndexerBackoff { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;searchDisableIndexingRemovableDrive&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to allow users to add locations on removable drives to libraries and to be indexed.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;searchDisableIndexingRemovableDrive&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean searchDisableIndexingRemovableDrive { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;searchEnableAutomaticIndexSizeManangement&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Specifies minimum amount of hard drive space on the same drive as the index location before indexing stops.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;searchEnableAutomaticIndexSizeManangement&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean searchEnableAutomaticIndexSizeManangement { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;diagnosticsDataSubmissionMode&quot; property, of type &quot;microsoft.graph.diagnosticDataSubmissionMode&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Gets or sets a value allowing the device to send diagnostic and usage telemetry data, such as Watson.</para>
        ///     <para type="description">
        ///          Valid values: &apos;userDefined&apos;, &apos;none&apos;, &apos;basic&apos;, &apos;enhanced&apos;, &apos;full&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.diagnosticDataSubmissionMode")]
        [Selectable]
        [ValidateSet(@"userDefined", @"none", @"basic", @"enhanced", @"full")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;diagnosticsDataSubmissionMode&quot; property, of type &quot;microsoft.graph.diagnosticDataSubmissionMode&quot;.")]
        public System.String diagnosticsDataSubmissionMode { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;oneDriveDisableFileSync&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Gets or sets a value allowing IT admins to prevent apps and features from working with files on OneDrive.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;oneDriveDisableFileSync&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean oneDriveDisableFileSync { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;smartScreenEnableAppInstallControl&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Allows IT Admins to control whether users are allowed to install apps from places other than the Store.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;smartScreenEnableAppInstallControl&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean smartScreenEnableAppInstallControl { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;personalizationDesktopImageUrl&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">A http or https Url to a jpg, jpeg or png image that needs to be downloaded and used as the Desktop Image or a file Url to a local image on the file system that needs to used as the Desktop Image.</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;personalizationDesktopImageUrl&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String personalizationDesktopImageUrl { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;personalizationLockScreenImageUrl&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">A http or https Url to a jpg, jpeg or png image that neeeds to be downloaded and used as the Lock Screen Image or a file Url to a local image on the file system that needs to be used as the Lock Screen Image.</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;personalizationLockScreenImageUrl&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String personalizationLockScreenImageUrl { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;bluetoothAllowedServices&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Specify a list of allowed Bluetooth services and profiles in hex formatted strings.</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [AllowEmptyCollection]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;bluetoothAllowedServices&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String[] bluetoothAllowedServices { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;bluetoothBlockAdvertising&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Whether or not to Block the user from using bluetooth advertising.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;bluetoothBlockAdvertising&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean bluetoothBlockAdvertising { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;bluetoothBlockDiscoverableMode&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Whether or not to Block the user from using bluetooth discoverable mode.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;bluetoothBlockDiscoverableMode&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean bluetoothBlockDiscoverableMode { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;bluetoothBlockPrePairing&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Whether or not to block specific bundled Bluetooth peripherals to automatically pair with the host device.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;bluetoothBlockPrePairing&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean bluetoothBlockPrePairing { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;edgeBlockAutofill&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block auto fill.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;edgeBlockAutofill&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean edgeBlockAutofill { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;edgeBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to Block the user from using the Edge browser.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;edgeBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean edgeBlocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;edgeCookiePolicy&quot; property, of type &quot;microsoft.graph.edgeCookiePolicy&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates which cookies to block in the Edge browser.</para>
        ///     <para type="description">
        ///          Valid values: &apos;userDefined&apos;, &apos;allow&apos;, &apos;blockThirdParty&apos;, &apos;blockAll&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.edgeCookiePolicy")]
        [Selectable]
        [ValidateSet(@"userDefined", @"allow", @"blockThirdParty", @"blockAll")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;edgeCookiePolicy&quot; property, of type &quot;microsoft.graph.edgeCookiePolicy&quot;.")]
        public System.String edgeCookiePolicy { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;edgeBlockDeveloperTools&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block developer tools in the Edge browser.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;edgeBlockDeveloperTools&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean edgeBlockDeveloperTools { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;edgeBlockSendingDoNotTrackHeader&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to Block the user from sending the do not track header.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;edgeBlockSendingDoNotTrackHeader&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean edgeBlockSendingDoNotTrackHeader { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;edgeBlockExtensions&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block extensions in the Edge browser.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;edgeBlockExtensions&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean edgeBlockExtensions { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;edgeBlockInPrivateBrowsing&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block InPrivate browsing on corporate networks, in the Edge browser.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;edgeBlockInPrivateBrowsing&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean edgeBlockInPrivateBrowsing { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;edgeBlockJavaScript&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to Block the user from using JavaScript.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;edgeBlockJavaScript&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean edgeBlockJavaScript { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;edgeBlockPasswordManager&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to Block password manager.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;edgeBlockPasswordManager&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean edgeBlockPasswordManager { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;edgeBlockAddressBarDropdown&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Block the address bar dropdown functionality in Microsoft Edge. Disable this settings to minimize network connections from Microsoft Edge to Microsoft services.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;edgeBlockAddressBarDropdown&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean edgeBlockAddressBarDropdown { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;edgeBlockCompatibilityList&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Block Microsoft compatibility list in Microsoft Edge. This list from Microsoft helps Edge properly display sites with known compatibility issues.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;edgeBlockCompatibilityList&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean edgeBlockCompatibilityList { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;edgeClearBrowsingDataOnExit&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Clear browsing data on exiting Microsoft Edge.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;edgeClearBrowsingDataOnExit&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean edgeClearBrowsingDataOnExit { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;edgeAllowStartPagesModification&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Allow users to change Start pages on Edge. Use the EdgeHomepageUrls to specify the Start pages that the user would see by default when they open Edge.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;edgeAllowStartPagesModification&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean edgeAllowStartPagesModification { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;edgeDisableFirstRunPage&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Block the Microsoft web page that opens on the first use of Microsoft Edge. This policy allows enterprises, like those enrolled in zero emissions configurations, to block this page.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;edgeDisableFirstRunPage&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean edgeDisableFirstRunPage { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;edgeBlockLiveTileDataCollection&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Block the collection of information by Microsoft for live tile creation when users pin a site to Start from Microsoft Edge.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;edgeBlockLiveTileDataCollection&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean edgeBlockLiveTileDataCollection { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;edgeSyncFavoritesWithInternetExplorer&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Enable favorites sync between Internet Explorer and Microsoft Edge. Additions, deletions, modifications and order changes to favorites are shared between browsers.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;edgeSyncFavoritesWithInternetExplorer&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean edgeSyncFavoritesWithInternetExplorer { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;cellularBlockDataWhenRoaming&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Whether or not to Block the user from using data over cellular while roaming.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;cellularBlockDataWhenRoaming&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean cellularBlockDataWhenRoaming { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;cellularBlockVpn&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Whether or not to Block the user from using VPN over cellular.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;cellularBlockVpn&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean cellularBlockVpn { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;cellularBlockVpnWhenRoaming&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Whether or not to Block the user from using VPN when roaming over cellular.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;cellularBlockVpnWhenRoaming&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean cellularBlockVpnWhenRoaming { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;defenderBlockEndUserAccess&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Whether or not to block end user access to Defender.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;defenderBlockEndUserAccess&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean defenderBlockEndUserAccess { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;defenderDaysBeforeDeletingQuarantinedMalware&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Number of days before deleting quarantined malware. Valid values 0 to 90</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;defenderDaysBeforeDeletingQuarantinedMalware&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 defenderDaysBeforeDeletingQuarantinedMalware { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;defenderDetectedMalwareActions&quot; property, of type &quot;microsoft.graph.defenderDetectedMalwareActions&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Gets or sets Defender’s actions to take on detected Malware per threat level.</para>
        /// </summary>
        [ODataType("microsoft.graph.defenderDetectedMalwareActions")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;defenderDetectedMalwareActions&quot; property, of type &quot;microsoft.graph.defenderDetectedMalwareActions&quot;.")]
        public System.Object defenderDetectedMalwareActions { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;defenderSystemScanSchedule&quot; property, of type &quot;microsoft.graph.weeklySchedule&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Defender day of the week for the system scan.</para>
        ///     <para type="description">
        ///          Valid values: &apos;userDefined&apos;, &apos;everyday&apos;, &apos;sunday&apos;, &apos;monday&apos;, &apos;tuesday&apos;, &apos;wednesday&apos;, &apos;thursday&apos;, &apos;friday&apos;, &apos;saturday&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.weeklySchedule")]
        [Selectable]
        [ValidateSet(@"userDefined", @"everyday", @"sunday", @"monday", @"tuesday", @"wednesday", @"thursday", @"friday", @"saturday")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;defenderSystemScanSchedule&quot; property, of type &quot;microsoft.graph.weeklySchedule&quot;.")]
        public System.String defenderSystemScanSchedule { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;defenderFilesAndFoldersToExclude&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Files and folder to exclude from scans and real time protection.</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [AllowEmptyCollection]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;defenderFilesAndFoldersToExclude&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String[] defenderFilesAndFoldersToExclude { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;defenderFileExtensionsToExclude&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">File extensions to exclude from scans and real time protection.</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [AllowEmptyCollection]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;defenderFileExtensionsToExclude&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String[] defenderFileExtensionsToExclude { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;defenderScanMaxCpu&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Max CPU usage percentage during scan. Valid values 0 to 100</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;defenderScanMaxCpu&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 defenderScanMaxCpu { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;defenderMonitorFileActivity&quot; property, of type &quot;microsoft.graph.defenderMonitorFileActivity&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Value for monitoring file activity.</para>
        ///     <para type="description">
        ///          Valid values: &apos;userDefined&apos;, &apos;disable&apos;, &apos;monitorAllFiles&apos;, &apos;monitorIncomingFilesOnly&apos;, &apos;monitorOutgoingFilesOnly&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.defenderMonitorFileActivity")]
        [Selectable]
        [ValidateSet(@"userDefined", @"disable", @"monitorAllFiles", @"monitorIncomingFilesOnly", @"monitorOutgoingFilesOnly")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;defenderMonitorFileActivity&quot; property, of type &quot;microsoft.graph.defenderMonitorFileActivity&quot;.")]
        public System.String defenderMonitorFileActivity { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;defenderProcessesToExclude&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Processes to exclude from scans and real time protection.</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [AllowEmptyCollection]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;defenderProcessesToExclude&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String[] defenderProcessesToExclude { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;defenderPromptForSampleSubmission&quot; property, of type &quot;microsoft.graph.defenderPromptForSampleSubmission&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">The configuration for how to prompt user for sample submission.</para>
        ///     <para type="description">
        ///          Valid values: &apos;userDefined&apos;, &apos;alwaysPrompt&apos;, &apos;promptBeforeSendingPersonalData&apos;, &apos;neverSendData&apos;, &apos;sendAllDataWithoutPrompting&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.defenderPromptForSampleSubmission")]
        [Selectable]
        [ValidateSet(@"userDefined", @"alwaysPrompt", @"promptBeforeSendingPersonalData", @"neverSendData", @"sendAllDataWithoutPrompting")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;defenderPromptForSampleSubmission&quot; property, of type &quot;microsoft.graph.defenderPromptForSampleSubmission&quot;.")]
        public System.String defenderPromptForSampleSubmission { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;defenderRequireBehaviorMonitoring&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to require behavior monitoring.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;defenderRequireBehaviorMonitoring&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean defenderRequireBehaviorMonitoring { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;defenderRequireCloudProtection&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to require cloud protection.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;defenderRequireCloudProtection&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean defenderRequireCloudProtection { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;defenderRequireNetworkInspectionSystem&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to require network inspection system.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;defenderRequireNetworkInspectionSystem&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean defenderRequireNetworkInspectionSystem { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;defenderRequireRealTimeMonitoring&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to require real time monitoring.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;defenderRequireRealTimeMonitoring&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean defenderRequireRealTimeMonitoring { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;defenderScanArchiveFiles&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to scan archive files.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;defenderScanArchiveFiles&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean defenderScanArchiveFiles { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;defenderScanDownloads&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to scan downloads.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;defenderScanDownloads&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean defenderScanDownloads { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;defenderScanNetworkFiles&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to scan files opened from a network folder.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;defenderScanNetworkFiles&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean defenderScanNetworkFiles { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;defenderScanIncomingMail&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to scan incoming mail messages.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;defenderScanIncomingMail&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean defenderScanIncomingMail { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;defenderScanMappedNetworkDrivesDuringFullScan&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to scan mapped network drives during full scan.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;defenderScanMappedNetworkDrivesDuringFullScan&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean defenderScanMappedNetworkDrivesDuringFullScan { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;defenderScanRemovableDrivesDuringFullScan&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to scan removable drives during full scan.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;defenderScanRemovableDrivesDuringFullScan&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean defenderScanRemovableDrivesDuringFullScan { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;defenderScanScriptsLoadedInInternetExplorer&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to scan scripts loaded in Internet Explorer browser.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;defenderScanScriptsLoadedInInternetExplorer&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean defenderScanScriptsLoadedInInternetExplorer { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;defenderSignatureUpdateIntervalInHours&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">The signature update interval in hours. Specify 0 not to check. Valid values 0 to 24</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;defenderSignatureUpdateIntervalInHours&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 defenderSignatureUpdateIntervalInHours { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;defenderScanType&quot; property, of type &quot;microsoft.graph.defenderScanType&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">The defender system scan type.</para>
        ///     <para type="description">
        ///          Valid values: &apos;userDefined&apos;, &apos;disabled&apos;, &apos;quick&apos;, &apos;full&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.defenderScanType")]
        [Selectable]
        [ValidateSet(@"userDefined", @"disabled", @"quick", @"full")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;defenderScanType&quot; property, of type &quot;microsoft.graph.defenderScanType&quot;.")]
        public System.String defenderScanType { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;defenderScheduledScanTime&quot; property, of type &quot;Edm.TimeOfDay&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">The defender time for the system scan.</para>
        /// </summary>
        [ODataType("Edm.TimeOfDay")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;defenderScheduledScanTime&quot; property, of type &quot;Edm.TimeOfDay&quot;.")]
        public System.TimeSpan defenderScheduledScanTime { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;defenderScheduledQuickScanTime&quot; property, of type &quot;Edm.TimeOfDay&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">The time to perform a daily quick scan.</para>
        /// </summary>
        [ODataType("Edm.TimeOfDay")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;defenderScheduledQuickScanTime&quot; property, of type &quot;Edm.TimeOfDay&quot;.")]
        public System.TimeSpan defenderScheduledQuickScanTime { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;defenderCloudBlockLevel&quot; property, of type &quot;microsoft.graph.defenderCloudBlockLevelType&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Specifies the level of cloud-delivered protection.</para>
        ///     <para type="description">
        ///          Valid values: &apos;notConfigured&apos;, &apos;high&apos;, &apos;highPlus&apos;, &apos;zeroTolerance&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.defenderCloudBlockLevelType")]
        [Selectable]
        [ValidateSet(@"notConfigured", @"high", @"highPlus", @"zeroTolerance")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;defenderCloudBlockLevel&quot; property, of type &quot;microsoft.graph.defenderCloudBlockLevelType&quot;.")]
        public System.String defenderCloudBlockLevel { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;lockScreenAllowTimeoutConfiguration&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Specify whether to show a user-configurable setting to control the screen timeout while on the lock screen of Windows 10 Mobile devices. If this policy is set to Allow, the value set by lockScreenTimeoutInSeconds is ignored.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;lockScreenAllowTimeoutConfiguration&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean lockScreenAllowTimeoutConfiguration { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;lockScreenBlockActionCenterNotifications&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block action center notifications over lock screen.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;lockScreenBlockActionCenterNotifications&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean lockScreenBlockActionCenterNotifications { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;lockScreenBlockCortana&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not the user can interact with Cortana using speech while the system is locked.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;lockScreenBlockCortana&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean lockScreenBlockCortana { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;lockScreenBlockToastNotifications&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether to allow toast notifications above the device lock screen.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;lockScreenBlockToastNotifications&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean lockScreenBlockToastNotifications { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;lockScreenTimeoutInSeconds&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Set the duration (in seconds) from the screen locking to the screen turning off for Windows 10 Mobile devices. Supported values are 11-1800. Valid values 11 to 1800</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;lockScreenTimeoutInSeconds&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 lockScreenTimeoutInSeconds { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;passwordRequireWhenResumeFromIdleState&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to require a password upon resuming from an idle state.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;passwordRequireWhenResumeFromIdleState&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean passwordRequireWhenResumeFromIdleState { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;privacyAdvertisingId&quot; property, of type &quot;microsoft.graph.stateManagementSetting&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Enables or disables the use of advertising ID. Added in Windows 10, version 1607.</para>
        ///     <para type="description">
        ///          Valid values: &apos;notConfigured&apos;, &apos;blocked&apos;, &apos;allowed&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.stateManagementSetting")]
        [Selectable]
        [ValidateSet(@"notConfigured", @"blocked", @"allowed")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;privacyAdvertisingId&quot; property, of type &quot;microsoft.graph.stateManagementSetting&quot;.")]
        public System.String privacyAdvertisingId { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;privacyAutoAcceptPairingAndConsentPrompts&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to allow the automatic acceptance of the pairing and privacy user consent dialog when launching apps.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;privacyAutoAcceptPairingAndConsentPrompts&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean privacyAutoAcceptPairingAndConsentPrompts { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;privacyBlockInputPersonalization&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the usage of cloud based speech services for Cortana, Dictation, or Store applications.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;privacyBlockInputPersonalization&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean privacyBlockInputPersonalization { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;startBlockUnpinningAppsFromTaskbar&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the user from unpinning apps from taskbar.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;startBlockUnpinningAppsFromTaskbar&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean startBlockUnpinningAppsFromTaskbar { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;startMenuAppListVisibility&quot; property, of type &quot;microsoft.graph.windowsStartMenuAppListVisibilityType&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Setting the value of this collapses the app list, removes the app list entirely, or disables the corresponding toggle in the Settings app.</para>
        ///     <para type="description">
        ///          Valid values: &apos;userDefined&apos;, &apos;collapse&apos;, &apos;remove&apos;, &apos;disableSettingsApp&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.windowsStartMenuAppListVisibilityType")]
        [Selectable]
        [ValidateSet(@"userDefined", @"collapse", @"remove", @"disableSettingsApp")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;startMenuAppListVisibility&quot; property, of type &quot;microsoft.graph.windowsStartMenuAppListVisibilityType&quot;.")]
        public System.String startMenuAppListVisibility { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;startMenuHideChangeAccountSettings&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Enabling this policy hides the change account setting from appearing in the user tile in the start menu.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;startMenuHideChangeAccountSettings&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean startMenuHideChangeAccountSettings { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;startMenuHideFrequentlyUsedApps&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Enabling this policy hides the most used apps from appearing on the start menu and disables the corresponding toggle in the Settings app.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;startMenuHideFrequentlyUsedApps&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean startMenuHideFrequentlyUsedApps { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;startMenuHideHibernate&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Enabling this policy hides hibernate from appearing in the power button in the start menu.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;startMenuHideHibernate&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean startMenuHideHibernate { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;startMenuHideLock&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Enabling this policy hides lock from appearing in the user tile in the start menu.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;startMenuHideLock&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean startMenuHideLock { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;startMenuHidePowerButton&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Enabling this policy hides the power button from appearing in the start menu.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;startMenuHidePowerButton&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean startMenuHidePowerButton { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;startMenuHideRecentJumpLists&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Enabling this policy hides recent jump lists from appearing on the start menu/taskbar and disables the corresponding toggle in the Settings app.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;startMenuHideRecentJumpLists&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean startMenuHideRecentJumpLists { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;startMenuHideRecentlyAddedApps&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Enabling this policy hides recently added apps from appearing on the start menu and disables the corresponding toggle in the Settings app.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;startMenuHideRecentlyAddedApps&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean startMenuHideRecentlyAddedApps { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;startMenuHideRestartOptions&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Enabling this policy hides “Restart/Update and Restart” from appearing in the power button in the start menu.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;startMenuHideRestartOptions&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean startMenuHideRestartOptions { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;startMenuHideShutDown&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Enabling this policy hides shut down/update and shut down from appearing in the power button in the start menu.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;startMenuHideShutDown&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean startMenuHideShutDown { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;startMenuHideSignOut&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Enabling this policy hides sign out from appearing in the user tile in the start menu.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;startMenuHideSignOut&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean startMenuHideSignOut { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;startMenuHideSleep&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Enabling this policy hides sleep from appearing in the power button in the start menu.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;startMenuHideSleep&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean startMenuHideSleep { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;startMenuHideSwitchAccount&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Enabling this policy hides switch account from appearing in the user tile in the start menu.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;startMenuHideSwitchAccount&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean startMenuHideSwitchAccount { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;startMenuHideUserTile&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Enabling this policy hides the user tile from appearing in the start menu.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;startMenuHideUserTile&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean startMenuHideUserTile { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;startMenuLayoutEdgeAssetsXml&quot; property, of type &quot;Edm.Binary&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">This policy setting allows you to import Edge assets to be used with startMenuLayoutXml policy. Start layout can contain secondary tile from Edge app which looks for Edge local asset file. Edge local asset would not exist and cause Edge secondary tile to appear empty in this case. This policy only gets applied when startMenuLayoutXml policy is modified. The value should be a UTF-8 Base64 encoded byte array.</para>
        /// </summary>
        [ODataType("Edm.Binary")]
        [Selectable]
        [AllowEmptyCollection]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;startMenuLayoutEdgeAssetsXml&quot; property, of type &quot;Edm.Binary&quot;.")]
        public System.Byte[] startMenuLayoutEdgeAssetsXml { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;startMenuLayoutXml&quot; property, of type &quot;Edm.Binary&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Allows admins to override the default Start menu layout and prevents the user from changing it. The layout is modified by specifying an XML file based on a layout modification schema. XML needs to be in a UTF8 encoded byte array format.</para>
        /// </summary>
        [ODataType("Edm.Binary")]
        [Selectable]
        [AllowEmptyCollection]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;startMenuLayoutXml&quot; property, of type &quot;Edm.Binary&quot;.")]
        public System.Byte[] startMenuLayoutXml { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;startMenuMode&quot; property, of type &quot;microsoft.graph.windowsStartMenuModeType&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Allows admins to decide how the Start menu is displayed.</para>
        ///     <para type="description">
        ///          Valid values: &apos;userDefined&apos;, &apos;fullScreen&apos;, &apos;nonFullScreen&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.windowsStartMenuModeType")]
        [Selectable]
        [ValidateSet(@"userDefined", @"fullScreen", @"nonFullScreen")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;startMenuMode&quot; property, of type &quot;microsoft.graph.windowsStartMenuModeType&quot;.")]
        public System.String startMenuMode { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;startMenuPinnedFolderDocuments&quot; property, of type &quot;microsoft.graph.visibilitySetting&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Enforces the visibility (Show/Hide) of the Documents folder shortcut on the Start menu.</para>
        ///     <para type="description">
        ///          Valid values: &apos;notConfigured&apos;, &apos;hide&apos;, &apos;show&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.visibilitySetting")]
        [Selectable]
        [ValidateSet(@"notConfigured", @"hide", @"show")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;startMenuPinnedFolderDocuments&quot; property, of type &quot;microsoft.graph.visibilitySetting&quot;.")]
        public System.String startMenuPinnedFolderDocuments { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;startMenuPinnedFolderDownloads&quot; property, of type &quot;microsoft.graph.visibilitySetting&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Enforces the visibility (Show/Hide) of the Downloads folder shortcut on the Start menu.</para>
        ///     <para type="description">
        ///          Valid values: &apos;notConfigured&apos;, &apos;hide&apos;, &apos;show&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.visibilitySetting")]
        [Selectable]
        [ValidateSet(@"notConfigured", @"hide", @"show")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;startMenuPinnedFolderDownloads&quot; property, of type &quot;microsoft.graph.visibilitySetting&quot;.")]
        public System.String startMenuPinnedFolderDownloads { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;startMenuPinnedFolderFileExplorer&quot; property, of type &quot;microsoft.graph.visibilitySetting&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Enforces the visibility (Show/Hide) of the FileExplorer shortcut on the Start menu.</para>
        ///     <para type="description">
        ///          Valid values: &apos;notConfigured&apos;, &apos;hide&apos;, &apos;show&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.visibilitySetting")]
        [Selectable]
        [ValidateSet(@"notConfigured", @"hide", @"show")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;startMenuPinnedFolderFileExplorer&quot; property, of type &quot;microsoft.graph.visibilitySetting&quot;.")]
        public System.String startMenuPinnedFolderFileExplorer { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;startMenuPinnedFolderHomeGroup&quot; property, of type &quot;microsoft.graph.visibilitySetting&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Enforces the visibility (Show/Hide) of the HomeGroup folder shortcut on the Start menu.</para>
        ///     <para type="description">
        ///          Valid values: &apos;notConfigured&apos;, &apos;hide&apos;, &apos;show&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.visibilitySetting")]
        [Selectable]
        [ValidateSet(@"notConfigured", @"hide", @"show")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;startMenuPinnedFolderHomeGroup&quot; property, of type &quot;microsoft.graph.visibilitySetting&quot;.")]
        public System.String startMenuPinnedFolderHomeGroup { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;startMenuPinnedFolderMusic&quot; property, of type &quot;microsoft.graph.visibilitySetting&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Enforces the visibility (Show/Hide) of the Music folder shortcut on the Start menu.</para>
        ///     <para type="description">
        ///          Valid values: &apos;notConfigured&apos;, &apos;hide&apos;, &apos;show&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.visibilitySetting")]
        [Selectable]
        [ValidateSet(@"notConfigured", @"hide", @"show")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;startMenuPinnedFolderMusic&quot; property, of type &quot;microsoft.graph.visibilitySetting&quot;.")]
        public System.String startMenuPinnedFolderMusic { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;startMenuPinnedFolderNetwork&quot; property, of type &quot;microsoft.graph.visibilitySetting&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Enforces the visibility (Show/Hide) of the Network folder shortcut on the Start menu.</para>
        ///     <para type="description">
        ///          Valid values: &apos;notConfigured&apos;, &apos;hide&apos;, &apos;show&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.visibilitySetting")]
        [Selectable]
        [ValidateSet(@"notConfigured", @"hide", @"show")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;startMenuPinnedFolderNetwork&quot; property, of type &quot;microsoft.graph.visibilitySetting&quot;.")]
        public System.String startMenuPinnedFolderNetwork { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;startMenuPinnedFolderPersonalFolder&quot; property, of type &quot;microsoft.graph.visibilitySetting&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Enforces the visibility (Show/Hide) of the PersonalFolder shortcut on the Start menu.</para>
        ///     <para type="description">
        ///          Valid values: &apos;notConfigured&apos;, &apos;hide&apos;, &apos;show&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.visibilitySetting")]
        [Selectable]
        [ValidateSet(@"notConfigured", @"hide", @"show")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;startMenuPinnedFolderPersonalFolder&quot; property, of type &quot;microsoft.graph.visibilitySetting&quot;.")]
        public System.String startMenuPinnedFolderPersonalFolder { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;startMenuPinnedFolderPictures&quot; property, of type &quot;microsoft.graph.visibilitySetting&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Enforces the visibility (Show/Hide) of the Pictures folder shortcut on the Start menu.</para>
        ///     <para type="description">
        ///          Valid values: &apos;notConfigured&apos;, &apos;hide&apos;, &apos;show&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.visibilitySetting")]
        [Selectable]
        [ValidateSet(@"notConfigured", @"hide", @"show")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;startMenuPinnedFolderPictures&quot; property, of type &quot;microsoft.graph.visibilitySetting&quot;.")]
        public System.String startMenuPinnedFolderPictures { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;startMenuPinnedFolderSettings&quot; property, of type &quot;microsoft.graph.visibilitySetting&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Enforces the visibility (Show/Hide) of the Settings folder shortcut on the Start menu.</para>
        ///     <para type="description">
        ///          Valid values: &apos;notConfigured&apos;, &apos;hide&apos;, &apos;show&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.visibilitySetting")]
        [Selectable]
        [ValidateSet(@"notConfigured", @"hide", @"show")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;startMenuPinnedFolderSettings&quot; property, of type &quot;microsoft.graph.visibilitySetting&quot;.")]
        public System.String startMenuPinnedFolderSettings { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;startMenuPinnedFolderVideos&quot; property, of type &quot;microsoft.graph.visibilitySetting&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Enforces the visibility (Show/Hide) of the Videos folder shortcut on the Start menu.</para>
        ///     <para type="description">
        ///          Valid values: &apos;notConfigured&apos;, &apos;hide&apos;, &apos;show&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.visibilitySetting")]
        [Selectable]
        [ValidateSet(@"notConfigured", @"hide", @"show")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;startMenuPinnedFolderVideos&quot; property, of type &quot;microsoft.graph.visibilitySetting&quot;.")]
        public System.String startMenuPinnedFolderVideos { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;settingsBlockSettingsApp&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block access to Settings app.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;settingsBlockSettingsApp&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean settingsBlockSettingsApp { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;settingsBlockSystemPage&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block access to System in Settings app.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;settingsBlockSystemPage&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean settingsBlockSystemPage { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;settingsBlockDevicesPage&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block access to Devices in Settings app.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;settingsBlockDevicesPage&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean settingsBlockDevicesPage { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;settingsBlockNetworkInternetPage&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block access to Network &amp; Internet in Settings app.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;settingsBlockNetworkInternetPage&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean settingsBlockNetworkInternetPage { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;settingsBlockPersonalizationPage&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block access to Personalization in Settings app.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;settingsBlockPersonalizationPage&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean settingsBlockPersonalizationPage { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;settingsBlockAccountsPage&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block access to Accounts in Settings app.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;settingsBlockAccountsPage&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean settingsBlockAccountsPage { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;settingsBlockTimeLanguagePage&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block access to Time &amp; Language in Settings app.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;settingsBlockTimeLanguagePage&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean settingsBlockTimeLanguagePage { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;settingsBlockEaseOfAccessPage&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block access to Ease of Access in Settings app.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;settingsBlockEaseOfAccessPage&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean settingsBlockEaseOfAccessPage { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;settingsBlockPrivacyPage&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block access to Privacy in Settings app.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;settingsBlockPrivacyPage&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean settingsBlockPrivacyPage { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;settingsBlockUpdateSecurityPage&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block access to Update &amp; Security in Settings app.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;settingsBlockUpdateSecurityPage&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean settingsBlockUpdateSecurityPage { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;settingsBlockAppsPage&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block access to Apps in Settings app.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;settingsBlockAppsPage&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean settingsBlockAppsPage { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;settingsBlockGamingPage&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block access to Gaming in Settings app.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;settingsBlockGamingPage&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean settingsBlockGamingPage { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;windowsSpotlightBlockConsumerSpecificFeatures&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Allows IT admins to block experiences that are typically for consumers only, such as Start suggestions, Membership notifications, Post-OOBE app install and redirect tiles.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;windowsSpotlightBlockConsumerSpecificFeatures&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean windowsSpotlightBlockConsumerSpecificFeatures { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;windowsSpotlightBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Allows IT admins to turn off all Windows Spotlight features</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;windowsSpotlightBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean windowsSpotlightBlocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;windowsSpotlightBlockOnActionCenter&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Block suggestions from Microsoft that show after each OS clean install, upgrade or in an on-going basis to introduce users to what is new or changed</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;windowsSpotlightBlockOnActionCenter&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean windowsSpotlightBlockOnActionCenter { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;windowsSpotlightBlockTailoredExperiences&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Block personalized content in Windows spotlight based on user’s device usage.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;windowsSpotlightBlockTailoredExperiences&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean windowsSpotlightBlockTailoredExperiences { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;windowsSpotlightBlockThirdPartyNotifications&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Block third party content delivered via Windows Spotlight</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;windowsSpotlightBlockThirdPartyNotifications&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean windowsSpotlightBlockThirdPartyNotifications { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;windowsSpotlightBlockWelcomeExperience&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Block Windows Spotlight Windows welcome experience</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;windowsSpotlightBlockWelcomeExperience&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean windowsSpotlightBlockWelcomeExperience { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;windowsSpotlightBlockWindowsTips&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Allows IT admins to turn off the popup of Windows Tips.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;windowsSpotlightBlockWindowsTips&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean windowsSpotlightBlockWindowsTips { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;windowsSpotlightConfigureOnLockScreen&quot; property, of type &quot;microsoft.graph.windowsSpotlightEnablementSettings&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Specifies the type of Spotlight</para>
        ///     <para type="description">
        ///          Valid values: &apos;notConfigured&apos;, &apos;disabled&apos;, &apos;enabled&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.windowsSpotlightEnablementSettings")]
        [Selectable]
        [ValidateSet(@"notConfigured", @"disabled", @"enabled")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;windowsSpotlightConfigureOnLockScreen&quot; property, of type &quot;microsoft.graph.windowsSpotlightEnablementSettings&quot;.")]
        public System.String windowsSpotlightConfigureOnLockScreen { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;networkProxyApplySettingsDeviceWide&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">If set, proxy settings will be applied to all processes and accounts in the device. Otherwise, it will be applied to the user account that’s enrolled into MDM.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;networkProxyApplySettingsDeviceWide&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean networkProxyApplySettingsDeviceWide { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;networkProxyDisableAutoDetect&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Disable automatic detection of settings. If enabled, the system will try to find the path to a proxy auto-config (PAC) script.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;networkProxyDisableAutoDetect&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean networkProxyDisableAutoDetect { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;networkProxyAutomaticConfigurationUrl&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Address to the proxy auto-config (PAC) script you want to use.</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;networkProxyAutomaticConfigurationUrl&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String networkProxyAutomaticConfigurationUrl { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;networkProxyServer&quot; property, of type &quot;microsoft.graph.windows10NetworkProxyServer&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Specifies manual proxy server settings.</para>
        /// </summary>
        [ODataType("microsoft.graph.windows10NetworkProxyServer")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;networkProxyServer&quot; property, of type &quot;microsoft.graph.windows10NetworkProxyServer&quot;.")]
        public System.Object networkProxyServer { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;antiTheftModeBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the user from selecting an AntiTheft mode preference (Windows 10 Mobile only).</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;antiTheftModeBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean antiTheftModeBlocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;connectedDevicesServiceBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Whether or not to block Connected Devices Service which enables discovery and connection to other devices, remote messaging, remote app sessions and other cross-device experiences.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;connectedDevicesServiceBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean connectedDevicesServiceBlocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;certificatesBlockManualRootCertificateInstallation&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Whether or not to Block the user from doing manual root certificate installation.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;certificatesBlockManualRootCertificateInstallation&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean certificatesBlockManualRootCertificateInstallation { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;copyPasteBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Whether or not to Block the user from using copy paste.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;copyPasteBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean copyPasteBlocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;cortanaBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Whether or not to Block the user from using Cortana.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;cortanaBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean cortanaBlocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;deviceManagementBlockFactoryResetOnMobile&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to Block the user from resetting their phone.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;deviceManagementBlockFactoryResetOnMobile&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean deviceManagementBlockFactoryResetOnMobile { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;deviceManagementBlockManualUnenroll&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to Block the user from doing manual un-enrollment from device management.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;deviceManagementBlockManualUnenroll&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean deviceManagementBlockManualUnenroll { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;safeSearchFilter&quot; property, of type &quot;microsoft.graph.safeSearchFilterType&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Specifies what filter level of safe search is required.</para>
        ///     <para type="description">
        ///          Valid values: &apos;userDefined&apos;, &apos;strict&apos;, &apos;moderate&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.safeSearchFilterType")]
        [Selectable]
        [ValidateSet(@"userDefined", @"strict", @"moderate")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;safeSearchFilter&quot; property, of type &quot;microsoft.graph.safeSearchFilterType&quot;.")]
        public System.String safeSearchFilter { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;edgeBlockPopups&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block popups.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;edgeBlockPopups&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean edgeBlockPopups { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;edgeBlockSearchSuggestions&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the user from using the search suggestions in the address bar.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;edgeBlockSearchSuggestions&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean edgeBlockSearchSuggestions { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;edgeBlockSendingIntranetTrafficToInternetExplorer&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to switch the intranet traffic from Edge to Internet Explorer. Note: the name of this property is misleading; the property is obsolete, use EdgeSendIntranetTrafficToInternetExplorer instead.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;edgeBlockSendingIntranetTrafficToInternetExplorer&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean edgeBlockSendingIntranetTrafficToInternetExplorer { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;edgeSendIntranetTrafficToInternetExplorer&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to switch the intranet traffic from Edge to Internet Explorer.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;edgeSendIntranetTrafficToInternetExplorer&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean edgeSendIntranetTrafficToInternetExplorer { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;edgeRequireSmartScreen&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to Require the user to use the smart screen filter.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;edgeRequireSmartScreen&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean edgeRequireSmartScreen { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;edgeEnterpriseModeSiteListLocation&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates the enterprise mode site list location. Could be a local file, local network or http location.</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;edgeEnterpriseModeSiteListLocation&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String edgeEnterpriseModeSiteListLocation { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;edgeFirstRunUrl&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">The first run URL for when Edge browser is opened for the first time.</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;edgeFirstRunUrl&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String edgeFirstRunUrl { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;edgeSearchEngine&quot; property, of type &quot;microsoft.graph.edgeSearchEngineBase&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Allows IT admins to set a default search engine for MDM-Controlled devices. Users can override this and change their default search engine provided the AllowSearchEngineCustomization policy is not set.</para>
        /// </summary>
        [ODataType("microsoft.graph.edgeSearchEngineBase", "microsoft.graph.edgeSearchEngine", "microsoft.graph.edgeSearchEngineCustom")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;edgeSearchEngine&quot; property, of type &quot;microsoft.graph.edgeSearchEngineBase&quot;.")]
        public System.Object edgeSearchEngine { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;edgeHomepageUrls&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">The list of URLs for homepages shodwn on MDM-enrolled devices on Edge browser.</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [AllowEmptyCollection]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;edgeHomepageUrls&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String[] edgeHomepageUrls { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;edgeBlockAccessToAboutFlags&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to prevent access to about flags on Edge browser.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;edgeBlockAccessToAboutFlags&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean edgeBlockAccessToAboutFlags { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;smartScreenBlockPromptOverride&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not users can override SmartScreen Filter warnings about potentially malicious websites.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;smartScreenBlockPromptOverride&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean smartScreenBlockPromptOverride { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;smartScreenBlockPromptOverrideForFiles&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not users can override the SmartScreen Filter warnings about downloading unverified files</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;smartScreenBlockPromptOverrideForFiles&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean smartScreenBlockPromptOverrideForFiles { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;webRtcBlockLocalhostIpAddress&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not user&apos;s localhost IP address is displayed while making phone calls using the WebRTC</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;webRtcBlockLocalhostIpAddress&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean webRtcBlockLocalhostIpAddress { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;internetSharingBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to Block the user from using internet sharing.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;internetSharingBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean internetSharingBlocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;settingsBlockAddProvisioningPackage&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the user from installing provisioning packages.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;settingsBlockAddProvisioningPackage&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean settingsBlockAddProvisioningPackage { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;settingsBlockRemoveProvisioningPackage&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the runtime configuration agent from removing provisioning packages.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;settingsBlockRemoveProvisioningPackage&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean settingsBlockRemoveProvisioningPackage { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;settingsBlockChangeSystemTime&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the user from changing date and time settings.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;settingsBlockChangeSystemTime&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean settingsBlockChangeSystemTime { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;settingsBlockEditDeviceName&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the user from editing the device name.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;settingsBlockEditDeviceName&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean settingsBlockEditDeviceName { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;settingsBlockChangeRegion&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the user from changing the region settings.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;settingsBlockChangeRegion&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean settingsBlockChangeRegion { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;settingsBlockChangeLanguage&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the user from changing the language settings.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;settingsBlockChangeLanguage&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean settingsBlockChangeLanguage { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;settingsBlockChangePowerSleep&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the user from changing power and sleep settings.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;settingsBlockChangePowerSleep&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean settingsBlockChangePowerSleep { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;microsoftAccountBlockSettingsSync&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to Block Microsoft account settings sync.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;microsoftAccountBlockSettingsSync&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean microsoftAccountBlockSettingsSync { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;resetProtectionModeBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to Block the user from reset protection mode.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;resetProtectionModeBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean resetProtectionModeBlocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;storageRequireMobileDeviceEncryption&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicating whether or not to require encryption on a mobile device.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;storageRequireMobileDeviceEncryption&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean storageRequireMobileDeviceEncryption { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;usbBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to Block the user from USB connection.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;usbBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean usbBlocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;voiceRecordingBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to Block the user from voice recording.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;voiceRecordingBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean voiceRecordingBlocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;wiFiBlockManualConfiguration&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to Block the user from using Wi-Fi manual configuration.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;wiFiBlockManualConfiguration&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean wiFiBlockManualConfiguration { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;wiFiScanInterval&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Specify how often devices scan for Wi-Fi networks. Supported values are 1-500, where 100 = default, and 500 = low frequency. Valid values 1 to 500</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;wiFiScanInterval&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 wiFiScanInterval { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;wirelessDisplayBlockProjectionToThisDevice&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to allow other devices from discovering this PC for projection.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;wirelessDisplayBlockProjectionToThisDevice&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean wirelessDisplayBlockProjectionToThisDevice { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;wirelessDisplayBlockUserInputFromReceiver&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to allow user input from wireless display receiver.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;wirelessDisplayBlockUserInputFromReceiver&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean wirelessDisplayBlockUserInputFromReceiver { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;wirelessDisplayRequirePinForPairing&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to require a PIN for new devices to initiate pairing.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;wirelessDisplayRequirePinForPairing&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean wirelessDisplayRequirePinForPairing { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;appsAllowTrustedAppsSideloading&quot; property, of type &quot;microsoft.graph.stateManagementSetting&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether apps from AppX packages signed with a trusted certificate can be side loaded.</para>
        ///     <para type="description">
        ///          Valid values: &apos;notConfigured&apos;, &apos;blocked&apos;, &apos;allowed&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.stateManagementSetting")]
        [Selectable]
        [ValidateSet(@"notConfigured", @"blocked", @"allowed")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;appsAllowTrustedAppsSideloading&quot; property, of type &quot;microsoft.graph.stateManagementSetting&quot;.")]
        public System.String appsAllowTrustedAppsSideloading { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;windowsStoreBlockAutoUpdate&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block automatic update of apps from Windows Store.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;windowsStoreBlockAutoUpdate&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean windowsStoreBlockAutoUpdate { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;developerUnlockSetting&quot; property, of type &quot;microsoft.graph.stateManagementSetting&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to allow developer unlock.</para>
        ///     <para type="description">
        ///          Valid values: &apos;notConfigured&apos;, &apos;blocked&apos;, &apos;allowed&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.stateManagementSetting")]
        [Selectable]
        [ValidateSet(@"notConfigured", @"blocked", @"allowed")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;developerUnlockSetting&quot; property, of type &quot;microsoft.graph.stateManagementSetting&quot;.")]
        public System.String developerUnlockSetting { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;sharedUserAppDataAllowed&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block multiple users of the same app to share data.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;sharedUserAppDataAllowed&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean sharedUserAppDataAllowed { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;appsBlockWindowsStoreOriginatedApps&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to disable the launch of all apps from Windows Store that came pre-installed or were downloaded.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;appsBlockWindowsStoreOriginatedApps&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean appsBlockWindowsStoreOriginatedApps { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;windowsStoreEnablePrivateStoreOnly&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to enable Private Store Only.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;windowsStoreEnablePrivateStoreOnly&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean windowsStoreEnablePrivateStoreOnly { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;storageRestrictAppDataToSystemVolume&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether application data is restricted to the system drive.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;storageRestrictAppDataToSystemVolume&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean storageRestrictAppDataToSystemVolume { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;storageRestrictAppInstallToSystemVolume&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether the installation of applications is restricted to the system drive.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;storageRestrictAppInstallToSystemVolume&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean storageRestrictAppInstallToSystemVolume { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;gameDvrBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block DVR and broadcasting.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;gameDvrBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean gameDvrBlocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;experienceBlockDeviceDiscovery&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to enable device discovery UX.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;experienceBlockDeviceDiscovery&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean experienceBlockDeviceDiscovery { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;experienceBlockErrorDialogWhenNoSIM&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to allow the error dialog from displaying if no SIM card is detected.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;experienceBlockErrorDialogWhenNoSIM&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean experienceBlockErrorDialogWhenNoSIM { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;experienceBlockTaskSwitcher&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to enable task switching on the device.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;experienceBlockTaskSwitcher&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean experienceBlockTaskSwitcher { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;logonBlockFastUserSwitching&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Disables the ability to quickly switch between users that are logged on simultaneously without logging off.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;logonBlockFastUserSwitching&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean logonBlockFastUserSwitching { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;tenantLockdownRequireNetworkDuringOutOfBoxExperience&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10GeneralConfiguration&quot; type.</para>
        ///     <para type="description">Whether the device is required to connect to the network.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10GeneralConfiguration", HelpMessage = @"The &quot;tenantLockdownRequireNetworkDuringOutOfBoxExperience&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean tenantLockdownRequireNetworkDuringOutOfBoxExperience { get; set; }

        /// <summary>
        ///     <para type="description">A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.windows10EndpointProtectionConfiguration&quot; type.</para>
        /// </summary>
        [Selectable]
        [Expandable]
        [ParameterSetSelector(@"microsoft.graph.windows10EndpointProtectionConfiguration")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", Mandatory = true, HelpMessage = @"A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.windows10EndpointProtectionConfiguration&quot; type.")]
        public System.Management.Automation.SwitchParameter windows10EndpointProtectionConfiguration { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;firewallBlockStatefulFTP&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10EndpointProtectionConfiguration&quot; type.</para>
        ///     <para type="description">Blocks stateful FTP connections to the device</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;firewallBlockStatefulFTP&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean firewallBlockStatefulFTP { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;firewallIdleTimeoutForSecurityAssociationInSeconds&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10EndpointProtectionConfiguration&quot; type.</para>
        ///     <para type="description">Configures the idle timeout for security associations, in seconds, from 300 to 3600 inclusive. This is the period after which security associations will expire and be deleted. Valid values 300 to 3600</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;firewallIdleTimeoutForSecurityAssociationInSeconds&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 firewallIdleTimeoutForSecurityAssociationInSeconds { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;firewallPreSharedKeyEncodingMethod&quot; property, of type &quot;microsoft.graph.firewallPreSharedKeyEncodingMethodType&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10EndpointProtectionConfiguration&quot; type.</para>
        ///     <para type="description">Select the preshared key encoding to be used</para>
        ///     <para type="description">
        ///          Valid values: &apos;deviceDefault&apos;, &apos;none&apos;, &apos;utF8&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.firewallPreSharedKeyEncodingMethodType")]
        [Selectable]
        [ValidateSet(@"deviceDefault", @"none", @"utF8")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;firewallPreSharedKeyEncodingMethod&quot; property, of type &quot;microsoft.graph.firewallPreSharedKeyEncodingMethodType&quot;.")]
        public System.String firewallPreSharedKeyEncodingMethod { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;firewallIPSecExemptionsAllowNeighborDiscovery&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10EndpointProtectionConfiguration&quot; type.</para>
        ///     <para type="description">Configures IPSec exemptions to allow neighbor discovery IPv6 ICMP type-codes</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;firewallIPSecExemptionsAllowNeighborDiscovery&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean firewallIPSecExemptionsAllowNeighborDiscovery { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;firewallIPSecExemptionsAllowICMP&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10EndpointProtectionConfiguration&quot; type.</para>
        ///     <para type="description">Configures IPSec exemptions to allow ICMP</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;firewallIPSecExemptionsAllowICMP&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean firewallIPSecExemptionsAllowICMP { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;firewallIPSecExemptionsAllowRouterDiscovery&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10EndpointProtectionConfiguration&quot; type.</para>
        ///     <para type="description">Configures IPSec exemptions to allow router discovery IPv6 ICMP type-codes</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;firewallIPSecExemptionsAllowRouterDiscovery&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean firewallIPSecExemptionsAllowRouterDiscovery { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;firewallIPSecExemptionsAllowDHCP&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10EndpointProtectionConfiguration&quot; type.</para>
        ///     <para type="description">Configures IPSec exemptions to allow both IPv4 and IPv6 DHCP traffic</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;firewallIPSecExemptionsAllowDHCP&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean firewallIPSecExemptionsAllowDHCP { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;firewallCertificateRevocationListCheckMethod&quot; property, of type &quot;microsoft.graph.firewallCertificateRevocationListCheckMethodType&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10EndpointProtectionConfiguration&quot; type.</para>
        ///     <para type="description">Specify how the certificate revocation list is to be enforced</para>
        ///     <para type="description">
        ///          Valid values: &apos;deviceDefault&apos;, &apos;none&apos;, &apos;attempt&apos;, &apos;require&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.firewallCertificateRevocationListCheckMethodType")]
        [Selectable]
        [ValidateSet(@"deviceDefault", @"none", @"attempt", @"require")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;firewallCertificateRevocationListCheckMethod&quot; property, of type &quot;microsoft.graph.firewallCertificateRevocationListCheckMethodType&quot;.")]
        public System.String firewallCertificateRevocationListCheckMethod { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;firewallMergeKeyingModuleSettings&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10EndpointProtectionConfiguration&quot; type.</para>
        ///     <para type="description">If an authentication set is not fully supported by a keying module, direct the module to ignore only unsupported authentication suites rather than the entire set</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;firewallMergeKeyingModuleSettings&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean firewallMergeKeyingModuleSettings { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;firewallPacketQueueingMethod&quot; property, of type &quot;microsoft.graph.firewallPacketQueueingMethodType&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10EndpointProtectionConfiguration&quot; type.</para>
        ///     <para type="description">Configures how packet queueing should be applied in the tunnel gateway scenario</para>
        ///     <para type="description">
        ///          Valid values: &apos;deviceDefault&apos;, &apos;disabled&apos;, &apos;queueInbound&apos;, &apos;queueOutbound&apos;, &apos;queueBoth&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.firewallPacketQueueingMethodType")]
        [Selectable]
        [ValidateSet(@"deviceDefault", @"disabled", @"queueInbound", @"queueOutbound", @"queueBoth")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;firewallPacketQueueingMethod&quot; property, of type &quot;microsoft.graph.firewallPacketQueueingMethodType&quot;.")]
        public System.String firewallPacketQueueingMethod { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;firewallProfileDomain&quot; property, of type &quot;microsoft.graph.windowsFirewallNetworkProfile&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10EndpointProtectionConfiguration&quot; type.</para>
        ///     <para type="description">Configures the firewall profile settings for domain networks</para>
        /// </summary>
        [ODataType("microsoft.graph.windowsFirewallNetworkProfile")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;firewallProfileDomain&quot; property, of type &quot;microsoft.graph.windowsFirewallNetworkProfile&quot;.")]
        public System.Object firewallProfileDomain { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;firewallProfilePublic&quot; property, of type &quot;microsoft.graph.windowsFirewallNetworkProfile&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10EndpointProtectionConfiguration&quot; type.</para>
        ///     <para type="description">Configures the firewall profile settings for public networks</para>
        /// </summary>
        [ODataType("microsoft.graph.windowsFirewallNetworkProfile")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;firewallProfilePublic&quot; property, of type &quot;microsoft.graph.windowsFirewallNetworkProfile&quot;.")]
        public System.Object firewallProfilePublic { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;firewallProfilePrivate&quot; property, of type &quot;microsoft.graph.windowsFirewallNetworkProfile&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10EndpointProtectionConfiguration&quot; type.</para>
        ///     <para type="description">Configures the firewall profile settings for private networks</para>
        /// </summary>
        [ODataType("microsoft.graph.windowsFirewallNetworkProfile")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;firewallProfilePrivate&quot; property, of type &quot;microsoft.graph.windowsFirewallNetworkProfile&quot;.")]
        public System.Object firewallProfilePrivate { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;defenderAttackSurfaceReductionExcludedPaths&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10EndpointProtectionConfiguration&quot; type.</para>
        ///     <para type="description">List of exe files and folders to be excluded from attack surface reduction rules</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [AllowEmptyCollection]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;defenderAttackSurfaceReductionExcludedPaths&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String[] defenderAttackSurfaceReductionExcludedPaths { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;defenderGuardedFoldersAllowedAppPaths&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10EndpointProtectionConfiguration&quot; type.</para>
        ///     <para type="description">List of paths to exe that are allowed to access protected folders</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [AllowEmptyCollection]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;defenderGuardedFoldersAllowedAppPaths&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String[] defenderGuardedFoldersAllowedAppPaths { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;defenderAdditionalGuardedFolders&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10EndpointProtectionConfiguration&quot; type.</para>
        ///     <para type="description">List of folder paths to be added to the list of protected folders</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [AllowEmptyCollection]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;defenderAdditionalGuardedFolders&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String[] defenderAdditionalGuardedFolders { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;defenderExploitProtectionXml&quot; property, of type &quot;Edm.Binary&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10EndpointProtectionConfiguration&quot; type.</para>
        ///     <para type="description">Xml content containing information regarding exploit protection details.</para>
        /// </summary>
        [ODataType("Edm.Binary")]
        [Selectable]
        [AllowEmptyCollection]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;defenderExploitProtectionXml&quot; property, of type &quot;Edm.Binary&quot;.")]
        public System.Byte[] defenderExploitProtectionXml { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;defenderExploitProtectionXmlFileName&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10EndpointProtectionConfiguration&quot; type.</para>
        ///     <para type="description">Name of the file from which DefenderExploitProtectionXml was obtained.</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;defenderExploitProtectionXmlFileName&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String defenderExploitProtectionXmlFileName { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;defenderSecurityCenterBlockExploitProtectionOverride&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10EndpointProtectionConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block user from overriding Exploit Protection settings.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;defenderSecurityCenterBlockExploitProtectionOverride&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean defenderSecurityCenterBlockExploitProtectionOverride { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;appLockerApplicationControl&quot; property, of type &quot;microsoft.graph.appLockerApplicationControlType&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10EndpointProtectionConfiguration&quot; type.</para>
        ///     <para type="description">Enables the Admin to choose what types of app to allow on devices.</para>
        ///     <para type="description">
        ///          Valid values: &apos;notConfigured&apos;, &apos;enforceComponentsAndStoreApps&apos;, &apos;auditComponentsAndStoreApps&apos;, &apos;enforceComponentsStoreAppsAndSmartlocker&apos;, &apos;auditComponentsStoreAppsAndSmartlocker&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.appLockerApplicationControlType")]
        [Selectable]
        [ValidateSet(@"notConfigured", @"enforceComponentsAndStoreApps", @"auditComponentsAndStoreApps", @"enforceComponentsStoreAppsAndSmartlocker", @"auditComponentsStoreAppsAndSmartlocker")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;appLockerApplicationControl&quot; property, of type &quot;microsoft.graph.appLockerApplicationControlType&quot;.")]
        public System.String appLockerApplicationControl { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;smartScreenEnableInShell&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10EndpointProtectionConfiguration&quot; type.</para>
        ///     <para type="description">Allows IT Admins to configure SmartScreen for Windows.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;smartScreenEnableInShell&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean smartScreenEnableInShell { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;smartScreenBlockOverrideForFiles&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10EndpointProtectionConfiguration&quot; type.</para>
        ///     <para type="description">Allows IT Admins to control whether users can can ignore SmartScreen warnings and run malicious files.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;smartScreenBlockOverrideForFiles&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean smartScreenBlockOverrideForFiles { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;applicationGuardEnabled&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10EndpointProtectionConfiguration&quot; type.</para>
        ///     <para type="description">Enable Windows Defender Application Guard</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;applicationGuardEnabled&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean applicationGuardEnabled { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;applicationGuardBlockFileTransfer&quot; property, of type &quot;microsoft.graph.applicationGuardBlockFileTransferType&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10EndpointProtectionConfiguration&quot; type.</para>
        ///     <para type="description">Block clipboard to transfer image file, text file or neither of them</para>
        ///     <para type="description">
        ///          Valid values: &apos;notConfigured&apos;, &apos;blockImageAndTextFile&apos;, &apos;blockImageFile&apos;, &apos;blockNone&apos;, &apos;blockTextFile&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.applicationGuardBlockFileTransferType")]
        [Selectable]
        [ValidateSet(@"notConfigured", @"blockImageAndTextFile", @"blockImageFile", @"blockNone", @"blockTextFile")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;applicationGuardBlockFileTransfer&quot; property, of type &quot;microsoft.graph.applicationGuardBlockFileTransferType&quot;.")]
        public System.String applicationGuardBlockFileTransfer { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;applicationGuardBlockNonEnterpriseContent&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10EndpointProtectionConfiguration&quot; type.</para>
        ///     <para type="description">Block enterprise sites to load non-enterprise content, such as third party plug-ins</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;applicationGuardBlockNonEnterpriseContent&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean applicationGuardBlockNonEnterpriseContent { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;applicationGuardAllowPersistence&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10EndpointProtectionConfiguration&quot; type.</para>
        ///     <para type="description">Allow persisting user generated data inside the App Guard Containter (favorites, cookies, web passwords, etc.)</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;applicationGuardAllowPersistence&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean applicationGuardAllowPersistence { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;applicationGuardForceAuditing&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10EndpointProtectionConfiguration&quot; type.</para>
        ///     <para type="description">Force auditing will persist Windows logs and events to meet security/compliance criteria (sample events are user login-logoff, use of privilege rights, software installation, system changes, etc.)</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;applicationGuardForceAuditing&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean applicationGuardForceAuditing { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;applicationGuardBlockClipboardSharing&quot; property, of type &quot;microsoft.graph.applicationGuardBlockClipboardSharingType&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10EndpointProtectionConfiguration&quot; type.</para>
        ///     <para type="description">Block clipboard to share data from Host to Container, or from Container to Host, or both ways, or neither ways.</para>
        ///     <para type="description">
        ///          Valid values: &apos;notConfigured&apos;, &apos;blockBoth&apos;, &apos;blockHostToContainer&apos;, &apos;blockContainerToHost&apos;, &apos;blockNone&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.applicationGuardBlockClipboardSharingType")]
        [Selectable]
        [ValidateSet(@"notConfigured", @"blockBoth", @"blockHostToContainer", @"blockContainerToHost", @"blockNone")]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;applicationGuardBlockClipboardSharing&quot; property, of type &quot;microsoft.graph.applicationGuardBlockClipboardSharingType&quot;.")]
        public System.String applicationGuardBlockClipboardSharing { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;applicationGuardAllowPrintToPDF&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10EndpointProtectionConfiguration&quot; type.</para>
        ///     <para type="description">Allow printing to PDF from Container</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;applicationGuardAllowPrintToPDF&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean applicationGuardAllowPrintToPDF { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;applicationGuardAllowPrintToXPS&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10EndpointProtectionConfiguration&quot; type.</para>
        ///     <para type="description">Allow printing to XPS from Container</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;applicationGuardAllowPrintToXPS&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean applicationGuardAllowPrintToXPS { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;applicationGuardAllowPrintToLocalPrinters&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10EndpointProtectionConfiguration&quot; type.</para>
        ///     <para type="description">Allow printing to Local Printers from Container</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;applicationGuardAllowPrintToLocalPrinters&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean applicationGuardAllowPrintToLocalPrinters { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;applicationGuardAllowPrintToNetworkPrinters&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10EndpointProtectionConfiguration&quot; type.</para>
        ///     <para type="description">Allow printing to Network Printers from Container</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;applicationGuardAllowPrintToNetworkPrinters&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean applicationGuardAllowPrintToNetworkPrinters { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;bitLockerDisableWarningForOtherDiskEncryption&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10EndpointProtectionConfiguration&quot; type.</para>
        ///     <para type="description">Allows the Admin to disable the warning prompt for other disk encryption on the user machines.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;bitLockerDisableWarningForOtherDiskEncryption&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean bitLockerDisableWarningForOtherDiskEncryption { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;bitLockerEnableStorageCardEncryptionOnMobile&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10EndpointProtectionConfiguration&quot; type.</para>
        ///     <para type="description">Allows the admin to require encryption to be turned on using BitLocker. This policy is valid only for a mobile SKU.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;bitLockerEnableStorageCardEncryptionOnMobile&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean bitLockerEnableStorageCardEncryptionOnMobile { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;bitLockerEncryptDevice&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10EndpointProtectionConfiguration&quot; type.</para>
        ///     <para type="description">Allows the admin to require encryption to be turned on using BitLocker.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;bitLockerEncryptDevice&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean bitLockerEncryptDevice { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;bitLockerRemovableDrivePolicy&quot; property, of type &quot;microsoft.graph.bitLockerRemovableDrivePolicy&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.windows10EndpointProtectionConfiguration&quot; type.</para>
        ///     <para type="description">BitLocker Removable Drive Policy.</para>
        /// </summary>
        [ODataType("microsoft.graph.bitLockerRemovableDrivePolicy")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.windows10EndpointProtectionConfiguration", HelpMessage = @"The &quot;bitLockerRemovableDrivePolicy&quot; property, of type &quot;microsoft.graph.bitLockerRemovableDrivePolicy&quot;.")]
        public System.Object bitLockerRemovableDrivePolicy { get; set; }

        /// <summary>
        ///     <para type="description">A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.macOSDeviceFeaturesConfiguration&quot; type.</para>
        /// </summary>
        [Selectable]
        [Expandable]
        [ParameterSetSelector(@"microsoft.graph.macOSDeviceFeaturesConfiguration")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSDeviceFeaturesConfiguration", Mandatory = true, HelpMessage = @"A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.macOSDeviceFeaturesConfiguration&quot; type.")]
        public System.Management.Automation.SwitchParameter macOSDeviceFeaturesConfiguration { get; set; }

        /// <summary>
        ///     <para type="description">A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.iosDeviceFeaturesConfiguration&quot; type.</para>
        /// </summary>
        [Selectable]
        [Expandable]
        [ParameterSetSelector(@"microsoft.graph.iosDeviceFeaturesConfiguration")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosDeviceFeaturesConfiguration", Mandatory = true, HelpMessage = @"A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.iosDeviceFeaturesConfiguration&quot; type.")]
        public System.Management.Automation.SwitchParameter iosDeviceFeaturesConfiguration { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;assetTagTemplate&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosDeviceFeaturesConfiguration&quot; type.</para>
        ///     <para type="description">Asset tag information for the device, displayed on the login window and lock screen.</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosDeviceFeaturesConfiguration", HelpMessage = @"The &quot;assetTagTemplate&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String assetTagTemplate { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;lockScreenFootnote&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosDeviceFeaturesConfiguration&quot; type.</para>
        ///     <para type="description">A footnote displayed on the login window and lock screen. Available in iOS 9.3.1 and later.</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosDeviceFeaturesConfiguration", HelpMessage = @"The &quot;lockScreenFootnote&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String lockScreenFootnote { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;homeScreenDockIcons&quot; property, of type &quot;microsoft.graph.iosHomeScreenItem&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosDeviceFeaturesConfiguration&quot; type.</para>
        ///     <para type="description">A list of app and folders to appear on the Home Screen Dock. This collection can contain a maximum of 500 elements.</para>
        /// </summary>
        [ODataType("microsoft.graph.iosHomeScreenItem", "microsoft.graph.iosHomeScreenApp", "microsoft.graph.iosHomeScreenFolder")]
        [Selectable]
        [AllowEmptyCollection]
        [Parameter(ParameterSetName = @"microsoft.graph.iosDeviceFeaturesConfiguration", HelpMessage = @"The &quot;homeScreenDockIcons&quot; property, of type &quot;microsoft.graph.iosHomeScreenItem&quot;.")]
        public System.Object[] homeScreenDockIcons { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;homeScreenPages&quot; property, of type &quot;microsoft.graph.iosHomeScreenPage&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosDeviceFeaturesConfiguration&quot; type.</para>
        ///     <para type="description">A list of pages on the Home Screen. This collection can contain a maximum of 500 elements.</para>
        /// </summary>
        [ODataType("microsoft.graph.iosHomeScreenPage")]
        [Selectable]
        [AllowEmptyCollection]
        [Parameter(ParameterSetName = @"microsoft.graph.iosDeviceFeaturesConfiguration", HelpMessage = @"The &quot;homeScreenPages&quot; property, of type &quot;microsoft.graph.iosHomeScreenPage&quot;.")]
        public System.Object[] homeScreenPages { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;notificationSettings&quot; property, of type &quot;microsoft.graph.iosNotificationSettings&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosDeviceFeaturesConfiguration&quot; type.</para>
        ///     <para type="description">Notification settings for each bundle id. Applicable to devices in supervised mode only (iOS 9.3 and later). This collection can contain a maximum of 500 elements.</para>
        /// </summary>
        [ODataType("microsoft.graph.iosNotificationSettings")]
        [Selectable]
        [AllowEmptyCollection]
        [Parameter(ParameterSetName = @"microsoft.graph.iosDeviceFeaturesConfiguration", HelpMessage = @"The &quot;notificationSettings&quot; property, of type &quot;microsoft.graph.iosNotificationSettings&quot;.")]
        public System.Object[] notificationSettings { get; set; }

        /// <summary>
        ///     <para type="description">A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.macOSGeneralDeviceConfiguration&quot; type.</para>
        /// </summary>
        [Selectable]
        [Expandable]
        [ParameterSetSelector(@"microsoft.graph.macOSGeneralDeviceConfiguration")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSGeneralDeviceConfiguration", Mandatory = true, HelpMessage = @"A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.macOSGeneralDeviceConfiguration&quot; type.")]
        public System.Management.Automation.SwitchParameter macOSGeneralDeviceConfiguration { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;emailInDomainSuffixes&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.macOSGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">An email address lacking a suffix that matches any of these strings will be considered out-of-domain.</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [AllowEmptyCollection]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSGeneralDeviceConfiguration", HelpMessage = @"The &quot;emailInDomainSuffixes&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;emailInDomainSuffixes&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String[] emailInDomainSuffixes { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;passwordMinutesOfInactivityBeforeLock&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.macOSGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Minutes of inactivity required before a password is required.</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSGeneralDeviceConfiguration", HelpMessage = @"The &quot;passwordMinutesOfInactivityBeforeLock&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 passwordMinutesOfInactivityBeforeLock { get; set; }

        /// <summary>
        ///     <para type="description">A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.macOSCustomConfiguration&quot; type.</para>
        /// </summary>
        [Selectable]
        [Expandable]
        [ParameterSetSelector(@"microsoft.graph.macOSCustomConfiguration")]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSCustomConfiguration", Mandatory = true, HelpMessage = @"A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.macOSCustomConfiguration&quot; type.")]
        public System.Management.Automation.SwitchParameter macOSCustomConfiguration { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;payloadName&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.macOSCustomConfiguration&quot; type.</para>
        ///     <para type="description">Name that is displayed to the user.</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSCustomConfiguration", HelpMessage = @"The &quot;payloadName&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosCustomConfiguration", HelpMessage = @"The &quot;payloadName&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String payloadName { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;payloadFileName&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.macOSCustomConfiguration&quot; type.</para>
        ///     <para type="description">Payload file name (*.mobileconfig | *.xml).</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSCustomConfiguration", HelpMessage = @"The &quot;payloadFileName&quot; property, of type &quot;Edm.String&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosCustomConfiguration", HelpMessage = @"The &quot;payloadFileName&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String payloadFileName { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;payload&quot; property, of type &quot;Edm.Binary&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.macOSCustomConfiguration&quot; type.</para>
        ///     <para type="description">Payload. (UTF8 encoded byte array)</para>
        /// </summary>
        [ODataType("Edm.Binary")]
        [Selectable]
        [AllowEmptyCollection]
        [Parameter(ParameterSetName = @"microsoft.graph.macOSCustomConfiguration", HelpMessage = @"The &quot;payload&quot; property, of type &quot;Edm.Binary&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosCustomConfiguration", HelpMessage = @"The &quot;payload&quot; property, of type &quot;Edm.Binary&quot;.")]
        public System.Byte[] payload { get; set; }

        /// <summary>
        ///     <para type="description">A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.iosUpdateConfiguration&quot; type.</para>
        /// </summary>
        [Selectable]
        [Expandable]
        [ParameterSetSelector(@"microsoft.graph.iosUpdateConfiguration")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosUpdateConfiguration", Mandatory = true, HelpMessage = @"A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.iosUpdateConfiguration&quot; type.")]
        public System.Management.Automation.SwitchParameter iosUpdateConfiguration { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;activeHoursStart&quot; property, of type &quot;Edm.TimeOfDay&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosUpdateConfiguration&quot; type.</para>
        ///     <para type="description">Active Hours Start (active hours mean the time window when updates install should not happen)</para>
        /// </summary>
        [ODataType("Edm.TimeOfDay")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosUpdateConfiguration", HelpMessage = @"The &quot;activeHoursStart&quot; property, of type &quot;Edm.TimeOfDay&quot;.")]
        public System.TimeSpan activeHoursStart { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;activeHoursEnd&quot; property, of type &quot;Edm.TimeOfDay&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosUpdateConfiguration&quot; type.</para>
        ///     <para type="description">Active Hours End (active hours mean the time window when updates install should not happen)</para>
        /// </summary>
        [ODataType("Edm.TimeOfDay")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosUpdateConfiguration", HelpMessage = @"The &quot;activeHoursEnd&quot; property, of type &quot;Edm.TimeOfDay&quot;.")]
        public System.TimeSpan activeHoursEnd { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;scheduledInstallDays&quot; property, of type &quot;microsoft.graph.dayOfWeek&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosUpdateConfiguration&quot; type.</para>
        ///     <para type="description">Days in week for which active hours are configured. This collection can contain a maximum of 7 elements.</para>
        ///     <para type="description">
        ///          Valid values: &apos;sunday&apos;, &apos;monday&apos;, &apos;tuesday&apos;, &apos;wednesday&apos;, &apos;thursday&apos;, &apos;friday&apos;, &apos;saturday&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.dayOfWeek")]
        [Selectable]
        [ValidateSet(@"sunday", @"monday", @"tuesday", @"wednesday", @"thursday", @"friday", @"saturday")]
        [AllowEmptyCollection]
        [Parameter(ParameterSetName = @"microsoft.graph.iosUpdateConfiguration", HelpMessage = @"The &quot;scheduledInstallDays&quot; property, of type &quot;microsoft.graph.dayOfWeek&quot;.")]
        public System.String[] scheduledInstallDays { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;utcTimeOffsetInMinutes&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosUpdateConfiguration&quot; type.</para>
        ///     <para type="description">UTC Time Offset indicated in minutes</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosUpdateConfiguration", HelpMessage = @"The &quot;utcTimeOffsetInMinutes&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 utcTimeOffsetInMinutes { get; set; }

        /// <summary>
        ///     <para type="description">A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        /// </summary>
        [Selectable]
        [Expandable]
        [ParameterSetSelector(@"microsoft.graph.iosGeneralDeviceConfiguration")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", Mandatory = true, HelpMessage = @"A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.")]
        public System.Management.Automation.SwitchParameter iosGeneralDeviceConfiguration { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;accountBlockModification&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to allow account modification when the device is in supervised mode.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;accountBlockModification&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean accountBlockModification { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;activationLockAllowWhenSupervised&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to allow activation lock when the device is in the supervised mode.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;activationLockAllowWhenSupervised&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean activationLockAllowWhenSupervised { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;airDropBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to allow AirDrop when the device is in supervised mode.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;airDropBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean airDropBlocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;airDropForceUnmanagedDropTarget&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to cause AirDrop to be considered an unmanaged drop target (iOS 9.0 and later).</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;airDropForceUnmanagedDropTarget&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean airDropForceUnmanagedDropTarget { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;airPlayForcePairingPasswordForOutgoingRequests&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to enforce all devices receiving AirPlay requests from this device to use a pairing password.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;airPlayForcePairingPasswordForOutgoingRequests&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean airPlayForcePairingPasswordForOutgoingRequests { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;appleWatchBlockPairing&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to allow Apple Watch pairing when the device is in supervised mode (iOS 9.0 and later).</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;appleWatchBlockPairing&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean appleWatchBlockPairing { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;appleWatchForceWristDetection&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to force a paired Apple Watch to use Wrist Detection (iOS 8.2 and later).</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;appleWatchForceWristDetection&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean appleWatchForceWristDetection { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;appleNewsBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the user from using News when the device is in supervised mode (iOS 9.0 and later).</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;appleNewsBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean appleNewsBlocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;appsSingleAppModeList&quot; property, of type &quot;microsoft.graph.appListItem&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Gets or sets the list of iOS apps allowed to autonomously enter Single App Mode. Supervised only. iOS 7.0 and later. This collection can contain a maximum of 500 elements.</para>
        /// </summary>
        [ODataType("microsoft.graph.appListItem")]
        [Selectable]
        [AllowEmptyCollection]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;appsSingleAppModeList&quot; property, of type &quot;microsoft.graph.appListItem&quot;.")]
        public System.Object[] appsSingleAppModeList { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;appsVisibilityList&quot; property, of type &quot;microsoft.graph.appListItem&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">List of apps in the visibility list (either visible/launchable apps list or hidden/unlaunchable apps list, controlled by AppsVisibilityListType) (iOS 9.3 and later). This collection can contain a maximum of 10000 elements.</para>
        /// </summary>
        [ODataType("microsoft.graph.appListItem")]
        [Selectable]
        [AllowEmptyCollection]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;appsVisibilityList&quot; property, of type &quot;microsoft.graph.appListItem&quot;.")]
        public System.Object[] appsVisibilityList { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;appsVisibilityListType&quot; property, of type &quot;microsoft.graph.appListType&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Type of list that is in the AppsVisibilityList.</para>
        ///     <para type="description">
        ///          Valid values: &apos;none&apos;, &apos;appsInListCompliant&apos;, &apos;appsNotInListCompliant&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.appListType")]
        [Selectable]
        [ValidateSet(@"none", @"appsInListCompliant", @"appsNotInListCompliant")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;appsVisibilityListType&quot; property, of type &quot;microsoft.graph.appListType&quot;.")]
        public System.String appsVisibilityListType { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;appStoreBlockAutomaticDownloads&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the automatic downloading of apps purchased on other devices when the device is in supervised mode (iOS 9.0 and later).</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;appStoreBlockAutomaticDownloads&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean appStoreBlockAutomaticDownloads { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;appStoreBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the user from using the App Store.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;appStoreBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean appStoreBlocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;appStoreBlockInAppPurchases&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the user from making in app purchases.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;appStoreBlockInAppPurchases&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean appStoreBlockInAppPurchases { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;appStoreBlockUIAppInstallation&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the App Store app, not restricting installation through Host apps. Applies to supervised mode only (iOS 9.0 and later).</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;appStoreBlockUIAppInstallation&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean appStoreBlockUIAppInstallation { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;appStoreRequirePassword&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to require a password when using the app store.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;appStoreRequirePassword&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean appStoreRequirePassword { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;bluetoothBlockModification&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to allow modification of Bluetooth settings when the device is in supervised mode (iOS 10.0 and later).</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;bluetoothBlockModification&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean bluetoothBlockModification { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;cellularBlockGlobalBackgroundFetchWhileRoaming&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block global background fetch while roaming.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;cellularBlockGlobalBackgroundFetchWhileRoaming&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean cellularBlockGlobalBackgroundFetchWhileRoaming { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;cellularBlockPerAppDataModification&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to allow changes to cellular app data usage settings when the device is in supervised mode.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;cellularBlockPerAppDataModification&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean cellularBlockPerAppDataModification { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;cellularBlockPersonalHotspot&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block Personal Hotspot.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;cellularBlockPersonalHotspot&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean cellularBlockPersonalHotspot { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;cellularBlockVoiceRoaming&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block voice roaming.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;cellularBlockVoiceRoaming&quot; property, of type &quot;Edm.Boolean&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;cellularBlockVoiceRoaming&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean cellularBlockVoiceRoaming { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;certificatesBlockUntrustedTlsCertificates&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block untrusted TLS certificates.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;certificatesBlockUntrustedTlsCertificates&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean certificatesBlockUntrustedTlsCertificates { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;classroomAppBlockRemoteScreenObservation&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to allow remote screen observation by Classroom app when the device is in supervised mode (iOS 9.3 and later).</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;classroomAppBlockRemoteScreenObservation&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean classroomAppBlockRemoteScreenObservation { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;classroomAppForceUnpromptedScreenObservation&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to automatically give permission to the teacher of a managed course on the Classroom app to view a student&apos;s screen without prompting when the device is in supervised mode.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;classroomAppForceUnpromptedScreenObservation&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean classroomAppForceUnpromptedScreenObservation { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;configurationProfileBlockChanges&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the user from installing configuration profiles and certificates interactively when the device is in supervised mode.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;configurationProfileBlockChanges&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean configurationProfileBlockChanges { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;definitionLookupBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block definition lookup when the device is in supervised mode (iOS 8.1.3 and later ).</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;definitionLookupBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean definitionLookupBlocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;deviceBlockEnableRestrictions&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to allow the user to enables restrictions in the device settings when the device is in supervised mode.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;deviceBlockEnableRestrictions&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean deviceBlockEnableRestrictions { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;deviceBlockEraseContentAndSettings&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to allow the use of the &apos;Erase all content and settings&apos; option on the device when the device is in supervised mode.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;deviceBlockEraseContentAndSettings&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean deviceBlockEraseContentAndSettings { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;deviceBlockNameModification&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to allow device name modification when the device is in supervised mode (iOS 9.0 and later).</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;deviceBlockNameModification&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean deviceBlockNameModification { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;diagnosticDataBlockSubmissionModification&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to allow diagnostics submission settings modification when the device is in supervised mode (iOS 9.3.2 and later).</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;diagnosticDataBlockSubmissionModification&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean diagnosticDataBlockSubmissionModification { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;documentsBlockManagedDocumentsInUnmanagedApps&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the user from viewing managed documents in unmanaged apps.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;documentsBlockManagedDocumentsInUnmanagedApps&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean documentsBlockManagedDocumentsInUnmanagedApps { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;documentsBlockUnmanagedDocumentsInManagedApps&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the user from viewing unmanaged documents in managed apps.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;documentsBlockUnmanagedDocumentsInManagedApps&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean documentsBlockUnmanagedDocumentsInManagedApps { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;enterpriseAppBlockTrust&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the user from trusting an enterprise app.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;enterpriseAppBlockTrust&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean enterpriseAppBlockTrust { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;enterpriseAppBlockTrustModification&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the user from modifying the enterprise app trust settings.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;enterpriseAppBlockTrustModification&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean enterpriseAppBlockTrustModification { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;faceTimeBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the user from using FaceTime.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;faceTimeBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean faceTimeBlocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;findMyFriendsBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block Find My Friends when the device is in supervised mode.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;findMyFriendsBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean findMyFriendsBlocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;gamingBlockGameCenterFriends&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the user from having friends in Game Center.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;gamingBlockGameCenterFriends&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean gamingBlockGameCenterFriends { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;gamingBlockMultiplayer&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the user from using multiplayer gaming.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;gamingBlockMultiplayer&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean gamingBlockMultiplayer { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;gameCenterBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the user from using Game Center when the device is in supervised mode.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;gameCenterBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean gameCenterBlocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;hostPairingBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">indicates whether or not to allow host pairing to control the devices an iOS device can pair with when the iOS device is in supervised mode.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;hostPairingBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean hostPairingBlocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;iBooksStoreBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the user from using the iBooks Store when the device is in supervised mode.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;iBooksStoreBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean iBooksStoreBlocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;iBooksStoreBlockErotica&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the user from downloading media from the iBookstore that has been tagged as erotica.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;iBooksStoreBlockErotica&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean iBooksStoreBlockErotica { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;iCloudBlockActivityContinuation&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block  the the user from continuing work they started on iOS device to another iOS or macOS device.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;iCloudBlockActivityContinuation&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean iCloudBlockActivityContinuation { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;iCloudBlockBackup&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block iCloud backup.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;iCloudBlockBackup&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean iCloudBlockBackup { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;iCloudBlockDocumentSync&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block iCloud document sync.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;iCloudBlockDocumentSync&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean iCloudBlockDocumentSync { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;iCloudBlockManagedAppsSync&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block Managed Apps Cloud Sync.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;iCloudBlockManagedAppsSync&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean iCloudBlockManagedAppsSync { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;iCloudBlockPhotoLibrary&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block iCloud Photo Library.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;iCloudBlockPhotoLibrary&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean iCloudBlockPhotoLibrary { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;iCloudBlockPhotoStreamSync&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block iCloud Photo Stream Sync.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;iCloudBlockPhotoStreamSync&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean iCloudBlockPhotoStreamSync { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;iCloudBlockSharedPhotoStream&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block Shared Photo Stream.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;iCloudBlockSharedPhotoStream&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean iCloudBlockSharedPhotoStream { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;iCloudRequireEncryptedBackup&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to require backups to iCloud be encrypted.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;iCloudRequireEncryptedBackup&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean iCloudRequireEncryptedBackup { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;iTunesBlockExplicitContent&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the user from accessing explicit content in iTunes and the App Store.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;iTunesBlockExplicitContent&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean iTunesBlockExplicitContent { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;iTunesBlockMusicService&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block Music service and revert Music app to classic mode when the device is in supervised mode (iOS 9.3 and later and macOS 10.12 and later).</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;iTunesBlockMusicService&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean iTunesBlockMusicService { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;iTunesBlockRadio&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the user from using iTunes Radio when the device is in supervised mode (iOS 9.3 and later).</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;iTunesBlockRadio&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean iTunesBlockRadio { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;keyboardBlockAutoCorrect&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block keyboard auto-correction when the device is in supervised mode (iOS 8.1.3 and later).</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;keyboardBlockAutoCorrect&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean keyboardBlockAutoCorrect { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;keyboardBlockDictation&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the user from using dictation input when the device is in supervised mode.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;keyboardBlockDictation&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean keyboardBlockDictation { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;keyboardBlockPredictive&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block predictive keyboards when device is in supervised mode (iOS 8.1.3 and later).</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;keyboardBlockPredictive&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean keyboardBlockPredictive { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;keyboardBlockShortcuts&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block keyboard shortcuts when the device is in supervised mode (iOS 9.0 and later).</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;keyboardBlockShortcuts&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean keyboardBlockShortcuts { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;keyboardBlockSpellCheck&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block keyboard spell-checking when the device is in supervised mode (iOS 8.1.3 and later).</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;keyboardBlockSpellCheck&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean keyboardBlockSpellCheck { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;kioskModeAllowAssistiveSpeak&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to allow assistive speak while in kiosk mode.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;kioskModeAllowAssistiveSpeak&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean kioskModeAllowAssistiveSpeak { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;kioskModeAllowAssistiveTouchSettings&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to allow access to the Assistive Touch Settings while in kiosk mode.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;kioskModeAllowAssistiveTouchSettings&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean kioskModeAllowAssistiveTouchSettings { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;kioskModeAllowAutoLock&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to allow device auto lock while in kiosk mode.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;kioskModeAllowAutoLock&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean kioskModeAllowAutoLock { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;kioskModeAllowColorInversionSettings&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to allow access to the Color Inversion Settings while in kiosk mode.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;kioskModeAllowColorInversionSettings&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean kioskModeAllowColorInversionSettings { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;kioskModeAllowRingerSwitch&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to allow use of the ringer switch while in kiosk mode.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;kioskModeAllowRingerSwitch&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean kioskModeAllowRingerSwitch { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;kioskModeAllowScreenRotation&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to allow screen rotation while in kiosk mode.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;kioskModeAllowScreenRotation&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean kioskModeAllowScreenRotation { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;kioskModeAllowSleepButton&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to allow use of the sleep button while in kiosk mode.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;kioskModeAllowSleepButton&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean kioskModeAllowSleepButton { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;kioskModeAllowTouchscreen&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to allow use of the touchscreen while in kiosk mode.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;kioskModeAllowTouchscreen&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean kioskModeAllowTouchscreen { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;kioskModeAllowVoiceOverSettings&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to allow access to the voice over settings while in kiosk mode.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;kioskModeAllowVoiceOverSettings&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean kioskModeAllowVoiceOverSettings { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;kioskModeAllowVolumeButtons&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to allow use of the volume buttons while in kiosk mode.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;kioskModeAllowVolumeButtons&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean kioskModeAllowVolumeButtons { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;kioskModeAllowZoomSettings&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to allow access to the zoom settings while in kiosk mode.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;kioskModeAllowZoomSettings&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean kioskModeAllowZoomSettings { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;kioskModeAppStoreUrl&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">URL in the app store to the app to use for kiosk mode. Use if KioskModeManagedAppId is not known.</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;kioskModeAppStoreUrl&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String kioskModeAppStoreUrl { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;kioskModeBuiltInAppId&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">ID for built-in apps to use for kiosk mode. Used when KioskModeManagedAppId and KioskModeAppStoreUrl are not set.</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;kioskModeBuiltInAppId&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String kioskModeBuiltInAppId { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;kioskModeRequireAssistiveTouch&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to require assistive touch while in kiosk mode.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;kioskModeRequireAssistiveTouch&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean kioskModeRequireAssistiveTouch { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;kioskModeRequireColorInversion&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to require color inversion while in kiosk mode.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;kioskModeRequireColorInversion&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean kioskModeRequireColorInversion { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;kioskModeRequireMonoAudio&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to require mono audio while in kiosk mode.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;kioskModeRequireMonoAudio&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean kioskModeRequireMonoAudio { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;kioskModeRequireVoiceOver&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to require voice over while in kiosk mode.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;kioskModeRequireVoiceOver&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean kioskModeRequireVoiceOver { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;kioskModeRequireZoom&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to require zoom while in kiosk mode.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;kioskModeRequireZoom&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean kioskModeRequireZoom { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;kioskModeManagedAppId&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Managed app id of the app to use for kiosk mode. If KioskModeManagedAppId is specified then KioskModeAppStoreUrl will be ignored.</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;kioskModeManagedAppId&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String kioskModeManagedAppId { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;lockScreenBlockControlCenter&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the user from using control center on the lock screen.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;lockScreenBlockControlCenter&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean lockScreenBlockControlCenter { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;lockScreenBlockNotificationView&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the user from using the notification view on the lock screen.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;lockScreenBlockNotificationView&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean lockScreenBlockNotificationView { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;lockScreenBlockPassbook&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the user from using passbook when the device is locked.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;lockScreenBlockPassbook&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean lockScreenBlockPassbook { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;lockScreenBlockTodayView&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the user from using the Today View on the lock screen.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;lockScreenBlockTodayView&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean lockScreenBlockTodayView { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;mediaContentRatingAustralia&quot; property, of type &quot;microsoft.graph.mediaContentRatingAustralia&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Media content rating settings for Australia</para>
        /// </summary>
        [ODataType("microsoft.graph.mediaContentRatingAustralia")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;mediaContentRatingAustralia&quot; property, of type &quot;microsoft.graph.mediaContentRatingAustralia&quot;.")]
        public System.Object mediaContentRatingAustralia { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;mediaContentRatingCanada&quot; property, of type &quot;microsoft.graph.mediaContentRatingCanada&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Media content rating settings for Canada</para>
        /// </summary>
        [ODataType("microsoft.graph.mediaContentRatingCanada")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;mediaContentRatingCanada&quot; property, of type &quot;microsoft.graph.mediaContentRatingCanada&quot;.")]
        public System.Object mediaContentRatingCanada { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;mediaContentRatingFrance&quot; property, of type &quot;microsoft.graph.mediaContentRatingFrance&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Media content rating settings for France</para>
        /// </summary>
        [ODataType("microsoft.graph.mediaContentRatingFrance")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;mediaContentRatingFrance&quot; property, of type &quot;microsoft.graph.mediaContentRatingFrance&quot;.")]
        public System.Object mediaContentRatingFrance { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;mediaContentRatingGermany&quot; property, of type &quot;microsoft.graph.mediaContentRatingGermany&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Media content rating settings for Germany</para>
        /// </summary>
        [ODataType("microsoft.graph.mediaContentRatingGermany")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;mediaContentRatingGermany&quot; property, of type &quot;microsoft.graph.mediaContentRatingGermany&quot;.")]
        public System.Object mediaContentRatingGermany { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;mediaContentRatingIreland&quot; property, of type &quot;microsoft.graph.mediaContentRatingIreland&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Media content rating settings for Ireland</para>
        /// </summary>
        [ODataType("microsoft.graph.mediaContentRatingIreland")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;mediaContentRatingIreland&quot; property, of type &quot;microsoft.graph.mediaContentRatingIreland&quot;.")]
        public System.Object mediaContentRatingIreland { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;mediaContentRatingJapan&quot; property, of type &quot;microsoft.graph.mediaContentRatingJapan&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Media content rating settings for Japan</para>
        /// </summary>
        [ODataType("microsoft.graph.mediaContentRatingJapan")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;mediaContentRatingJapan&quot; property, of type &quot;microsoft.graph.mediaContentRatingJapan&quot;.")]
        public System.Object mediaContentRatingJapan { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;mediaContentRatingNewZealand&quot; property, of type &quot;microsoft.graph.mediaContentRatingNewZealand&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Media content rating settings for New Zealand</para>
        /// </summary>
        [ODataType("microsoft.graph.mediaContentRatingNewZealand")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;mediaContentRatingNewZealand&quot; property, of type &quot;microsoft.graph.mediaContentRatingNewZealand&quot;.")]
        public System.Object mediaContentRatingNewZealand { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;mediaContentRatingUnitedKingdom&quot; property, of type &quot;microsoft.graph.mediaContentRatingUnitedKingdom&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Media content rating settings for United Kingdom</para>
        /// </summary>
        [ODataType("microsoft.graph.mediaContentRatingUnitedKingdom")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;mediaContentRatingUnitedKingdom&quot; property, of type &quot;microsoft.graph.mediaContentRatingUnitedKingdom&quot;.")]
        public System.Object mediaContentRatingUnitedKingdom { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;mediaContentRatingUnitedStates&quot; property, of type &quot;microsoft.graph.mediaContentRatingUnitedStates&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Media content rating settings for United States</para>
        /// </summary>
        [ODataType("microsoft.graph.mediaContentRatingUnitedStates")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;mediaContentRatingUnitedStates&quot; property, of type &quot;microsoft.graph.mediaContentRatingUnitedStates&quot;.")]
        public System.Object mediaContentRatingUnitedStates { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;networkUsageRules&quot; property, of type &quot;microsoft.graph.iosNetworkUsageRule&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">List of managed apps and the network rules that applies to them. This collection can contain a maximum of 1000 elements.</para>
        /// </summary>
        [ODataType("microsoft.graph.iosNetworkUsageRule")]
        [Selectable]
        [AllowEmptyCollection]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;networkUsageRules&quot; property, of type &quot;microsoft.graph.iosNetworkUsageRule&quot;.")]
        public System.Object[] networkUsageRules { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;mediaContentRatingApps&quot; property, of type &quot;microsoft.graph.ratingAppsType&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Media content rating settings for Apps</para>
        ///     <para type="description">
        ///          Valid values: &apos;allAllowed&apos;, &apos;allBlocked&apos;, &apos;agesAbove4&apos;, &apos;agesAbove9&apos;, &apos;agesAbove12&apos;, &apos;agesAbove17&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.ratingAppsType")]
        [Selectable]
        [ValidateSet(@"allAllowed", @"allBlocked", @"agesAbove4", @"agesAbove9", @"agesAbove12", @"agesAbove17")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;mediaContentRatingApps&quot; property, of type &quot;microsoft.graph.ratingAppsType&quot;.")]
        public System.String mediaContentRatingApps { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;messagesBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the user from using the Messages app on the supervised device.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;messagesBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean messagesBlocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;notificationsBlockSettingsModification&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to allow notifications settings modification (iOS 9.3 and later).</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;notificationsBlockSettingsModification&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean notificationsBlockSettingsModification { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;passcodeBlockFingerprintUnlock&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block fingerprint unlock.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;passcodeBlockFingerprintUnlock&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean passcodeBlockFingerprintUnlock { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;passcodeBlockFingerprintModification&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Block modification of registered Touch ID fingerprints when in supervised mode.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;passcodeBlockFingerprintModification&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean passcodeBlockFingerprintModification { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;passcodeBlockModification&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to allow passcode modification on the supervised device (iOS 9.0 and later).</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;passcodeBlockModification&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean passcodeBlockModification { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;passcodeBlockSimple&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block simple passcodes.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;passcodeBlockSimple&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean passcodeBlockSimple { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;passcodeExpirationDays&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Number of days before the passcode expires. Valid values 1 to 65535</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;passcodeExpirationDays&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 passcodeExpirationDays { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;passcodeMinimumLength&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Minimum length of passcode. Valid values 4 to 14</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;passcodeMinimumLength&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 passcodeMinimumLength { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;passcodeMinutesOfInactivityBeforeLock&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Minutes of inactivity before a passcode is required.</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;passcodeMinutesOfInactivityBeforeLock&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 passcodeMinutesOfInactivityBeforeLock { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;passcodeMinutesOfInactivityBeforeScreenTimeout&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Minutes of inactivity before the screen times out.</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;passcodeMinutesOfInactivityBeforeScreenTimeout&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 passcodeMinutesOfInactivityBeforeScreenTimeout { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;passcodeMinimumCharacterSetCount&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Number of character sets a passcode must contain. Valid values 0 to 4</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;passcodeMinimumCharacterSetCount&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 passcodeMinimumCharacterSetCount { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;passcodePreviousPasscodeBlockCount&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Number of previous passcodes to block. Valid values 1 to 24</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;passcodePreviousPasscodeBlockCount&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 passcodePreviousPasscodeBlockCount { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;passcodeSignInFailureCountBeforeWipe&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Number of sign in failures allowed before wiping the device. Valid values 4 to 11</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;passcodeSignInFailureCountBeforeWipe&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 passcodeSignInFailureCountBeforeWipe { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;passcodeRequiredType&quot; property, of type &quot;microsoft.graph.requiredPasswordType&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Type of passcode that is required.</para>
        ///     <para type="description">
        ///          Valid values: &apos;deviceDefault&apos;, &apos;alphanumeric&apos;, &apos;numeric&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.requiredPasswordType")]
        [Selectable]
        [ValidateSet(@"deviceDefault", @"alphanumeric", @"numeric")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;passcodeRequiredType&quot; property, of type &quot;microsoft.graph.requiredPasswordType&quot;.")]
        public System.String passcodeRequiredType { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;passcodeRequired&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to require a passcode.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;passcodeRequired&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean passcodeRequired { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;podcastsBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the user from using podcasts on the supervised device (iOS 8.0 and later).</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;podcastsBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean podcastsBlocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;safariBlockAutofill&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the user from using Auto fill in Safari.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;safariBlockAutofill&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean safariBlockAutofill { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;safariBlockJavaScript&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block JavaScript in Safari.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;safariBlockJavaScript&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean safariBlockJavaScript { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;safariBlockPopups&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block popups in Safari.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;safariBlockPopups&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean safariBlockPopups { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;safariBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the user from using Safari.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;safariBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean safariBlocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;safariCookieSettings&quot; property, of type &quot;microsoft.graph.webBrowserCookieSettings&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Cookie settings for Safari.</para>
        ///     <para type="description">
        ///          Valid values: &apos;browserDefault&apos;, &apos;blockAlways&apos;, &apos;allowCurrentWebSite&apos;, &apos;allowFromWebsitesVisited&apos;, &apos;allowAlways&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.webBrowserCookieSettings")]
        [Selectable]
        [ValidateSet(@"browserDefault", @"blockAlways", @"allowCurrentWebSite", @"allowFromWebsitesVisited", @"allowAlways")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;safariCookieSettings&quot; property, of type &quot;microsoft.graph.webBrowserCookieSettings&quot;.")]
        public System.String safariCookieSettings { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;safariManagedDomains&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">URLs matching the patterns listed here will be considered managed.</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [AllowEmptyCollection]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;safariManagedDomains&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String[] safariManagedDomains { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;safariPasswordAutoFillDomains&quot; property, of type &quot;Edm.String&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Users can save passwords in Safari only from URLs matching the patterns listed here. Applies to devices in supervised mode (iOS 9.3 and later).</para>
        /// </summary>
        [ODataType("Edm.String")]
        [Selectable]
        [AllowEmptyCollection]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;safariPasswordAutoFillDomains&quot; property, of type &quot;Edm.String&quot;.")]
        public System.String[] safariPasswordAutoFillDomains { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;safariRequireFraudWarning&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to require fraud warning in Safari.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;safariRequireFraudWarning&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean safariRequireFraudWarning { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;siriBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the user from using Siri.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;siriBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean siriBlocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;siriBlockedWhenLocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the user from using Siri when locked.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;siriBlockedWhenLocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean siriBlockedWhenLocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;siriBlockUserGeneratedContent&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block Siri from querying user-generated content when used on a supervised device.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;siriBlockUserGeneratedContent&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean siriBlockUserGeneratedContent { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;siriRequireProfanityFilter&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to prevent Siri from dictating, or speaking profane language on supervised device.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;siriRequireProfanityFilter&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean siriRequireProfanityFilter { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;spotlightBlockInternetResults&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block Spotlight search from returning internet results on supervised device.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;spotlightBlockInternetResults&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean spotlightBlockInternetResults { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;voiceDialingBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block voice dialing.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;voiceDialingBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;voiceDialingBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean voiceDialingBlocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;wallpaperBlockModification&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to allow wallpaper modification on supervised device (iOS 9.0 and later) .</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;wallpaperBlockModification&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean wallpaperBlockModification { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;wiFiConnectOnlyToConfiguredNetworks&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.iosGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to force the device to use only Wi-Fi networks from configuration profiles when the device is in supervised mode.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.iosGeneralDeviceConfiguration", HelpMessage = @"The &quot;wiFiConnectOnlyToConfiguredNetworks&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean wiFiConnectOnlyToConfiguredNetworks { get; set; }

        /// <summary>
        ///     <para type="description">A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.iosCustomConfiguration&quot; type.</para>
        /// </summary>
        [Selectable]
        [Expandable]
        [ParameterSetSelector(@"microsoft.graph.iosCustomConfiguration")]
        [Parameter(ParameterSetName = @"microsoft.graph.iosCustomConfiguration", Mandatory = true, HelpMessage = @"A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.iosCustomConfiguration&quot; type.")]
        public System.Management.Automation.SwitchParameter iosCustomConfiguration { get; set; }

        /// <summary>
        ///     <para type="description">A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.androidWorkProfileGeneralDeviceConfiguration&quot; type.</para>
        /// </summary>
        [Selectable]
        [Expandable]
        [ParameterSetSelector(@"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", Mandatory = true, HelpMessage = @"A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.androidWorkProfileGeneralDeviceConfiguration&quot; type.")]
        public System.Management.Automation.SwitchParameter androidWorkProfileGeneralDeviceConfiguration { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;passwordBlockFingerprintUnlock&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidWorkProfileGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block fingerprint unlock.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;passwordBlockFingerprintUnlock&quot; property, of type &quot;Edm.Boolean&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;passwordBlockFingerprintUnlock&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean passwordBlockFingerprintUnlock { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;passwordBlockTrustAgents&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidWorkProfileGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block Smart Lock and other trust agents.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;passwordBlockTrustAgents&quot; property, of type &quot;Edm.Boolean&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;passwordBlockTrustAgents&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean passwordBlockTrustAgents { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;workProfileDataSharingType&quot; property, of type &quot;microsoft.graph.androidWorkProfileCrossProfileDataSharingType&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidWorkProfileGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Type of data sharing that is allowed.</para>
        ///     <para type="description">
        ///          Valid values: &apos;deviceDefault&apos;, &apos;preventAny&apos;, &apos;allowPersonalToWork&apos;, &apos;noRestrictions&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.androidWorkProfileCrossProfileDataSharingType")]
        [Selectable]
        [ValidateSet(@"deviceDefault", @"preventAny", @"allowPersonalToWork", @"noRestrictions")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;workProfileDataSharingType&quot; property, of type &quot;microsoft.graph.androidWorkProfileCrossProfileDataSharingType&quot;.")]
        public System.String workProfileDataSharingType { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;workProfileBlockNotificationsWhileDeviceLocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidWorkProfileGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block notifications while device locked.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;workProfileBlockNotificationsWhileDeviceLocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean workProfileBlockNotificationsWhileDeviceLocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;workProfileBlockAddingAccounts&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidWorkProfileGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Block users from adding/removing accounts in work profile.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;workProfileBlockAddingAccounts&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean workProfileBlockAddingAccounts { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;workProfileBluetoothEnableContactSharing&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidWorkProfileGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Allow bluetooth devices to access enterprise contacts.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;workProfileBluetoothEnableContactSharing&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean workProfileBluetoothEnableContactSharing { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;workProfileBlockScreenCapture&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidWorkProfileGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Block screen capture in work profile.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;workProfileBlockScreenCapture&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean workProfileBlockScreenCapture { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;workProfileBlockCrossProfileCallerId&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidWorkProfileGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Block display work profile caller ID in personal profile.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;workProfileBlockCrossProfileCallerId&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean workProfileBlockCrossProfileCallerId { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;workProfileBlockCamera&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidWorkProfileGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Block work profile camera.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;workProfileBlockCamera&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean workProfileBlockCamera { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;workProfileBlockCrossProfileContactsSearch&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidWorkProfileGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Block work profile contacts availability in personal profile.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;workProfileBlockCrossProfileContactsSearch&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean workProfileBlockCrossProfileContactsSearch { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;workProfileBlockCrossProfileCopyPaste&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidWorkProfileGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Boolean that indicates if the setting disallow cross profile copy/paste is enabled.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;workProfileBlockCrossProfileCopyPaste&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean workProfileBlockCrossProfileCopyPaste { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;workProfileDefaultAppPermissionPolicy&quot; property, of type &quot;microsoft.graph.androidWorkProfileDefaultAppPermissionPolicyType&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidWorkProfileGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Type of password that is required.</para>
        ///     <para type="description">
        ///          Valid values: &apos;deviceDefault&apos;, &apos;prompt&apos;, &apos;autoGrant&apos;, &apos;autoDeny&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.androidWorkProfileDefaultAppPermissionPolicyType")]
        [Selectable]
        [ValidateSet(@"deviceDefault", @"prompt", @"autoGrant", @"autoDeny")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;workProfileDefaultAppPermissionPolicy&quot; property, of type &quot;microsoft.graph.androidWorkProfileDefaultAppPermissionPolicyType&quot;.")]
        public System.String workProfileDefaultAppPermissionPolicy { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;workProfilePasswordBlockFingerprintUnlock&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidWorkProfileGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block fingerprint unlock for work profile.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;workProfilePasswordBlockFingerprintUnlock&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean workProfilePasswordBlockFingerprintUnlock { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;workProfilePasswordBlockTrustAgents&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidWorkProfileGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block Smart Lock and other trust agents for work profile.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;workProfilePasswordBlockTrustAgents&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean workProfilePasswordBlockTrustAgents { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;workProfilePasswordExpirationDays&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidWorkProfileGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Number of days before the work profile password expires. Valid values 1 to 365</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;workProfilePasswordExpirationDays&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 workProfilePasswordExpirationDays { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;workProfilePasswordMinimumLength&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidWorkProfileGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Minimum length of work profile password. Valid values 4 to 16</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;workProfilePasswordMinimumLength&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 workProfilePasswordMinimumLength { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;workProfilePasswordMinNumericCharacters&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidWorkProfileGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Minimum # of numeric characters required in work profile password. Valid values 1 to 10</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;workProfilePasswordMinNumericCharacters&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 workProfilePasswordMinNumericCharacters { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;workProfilePasswordMinNonLetterCharacters&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidWorkProfileGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Minimum # of non-letter characters required in work profile password. Valid values 1 to 10</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;workProfilePasswordMinNonLetterCharacters&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 workProfilePasswordMinNonLetterCharacters { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;workProfilePasswordMinLetterCharacters&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidWorkProfileGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Minimum # of letter characters required in work profile password. Valid values 1 to 10</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;workProfilePasswordMinLetterCharacters&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 workProfilePasswordMinLetterCharacters { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;workProfilePasswordMinLowerCaseCharacters&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidWorkProfileGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Minimum # of lower-case characters required in work profile password. Valid values 1 to 10</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;workProfilePasswordMinLowerCaseCharacters&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 workProfilePasswordMinLowerCaseCharacters { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;workProfilePasswordMinUpperCaseCharacters&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidWorkProfileGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Minimum # of upper-case characters required in work profile password. Valid values 1 to 10</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;workProfilePasswordMinUpperCaseCharacters&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 workProfilePasswordMinUpperCaseCharacters { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;workProfilePasswordMinSymbolCharacters&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidWorkProfileGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Minimum # of symbols required in work profile password. Valid values 1 to 10</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;workProfilePasswordMinSymbolCharacters&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 workProfilePasswordMinSymbolCharacters { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;workProfilePasswordMinutesOfInactivityBeforeScreenTimeout&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidWorkProfileGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Minutes of inactivity before the screen times out.</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;workProfilePasswordMinutesOfInactivityBeforeScreenTimeout&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 workProfilePasswordMinutesOfInactivityBeforeScreenTimeout { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;workProfilePasswordPreviousPasswordBlockCount&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidWorkProfileGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Number of previous work profile passwords to block. Valid values 0 to 24</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;workProfilePasswordPreviousPasswordBlockCount&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 workProfilePasswordPreviousPasswordBlockCount { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;workProfilePasswordSignInFailureCountBeforeFactoryReset&quot; property, of type &quot;Edm.Int32&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidWorkProfileGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Number of sign in failures allowed before work profile is removed and all corporate data deleted. Valid values 1 to 16</para>
        /// </summary>
        [ODataType("Edm.Int32")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;workProfilePasswordSignInFailureCountBeforeFactoryReset&quot; property, of type &quot;Edm.Int32&quot;.")]
        public System.Int32 workProfilePasswordSignInFailureCountBeforeFactoryReset { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;workProfilePasswordRequiredType&quot; property, of type &quot;microsoft.graph.androidWorkProfileRequiredPasswordType&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidWorkProfileGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Type of work profile password that is required.</para>
        ///     <para type="description">
        ///          Valid values: &apos;deviceDefault&apos;, &apos;lowSecurityBiometric&apos;, &apos;required&apos;, &apos;atLeastNumeric&apos;, &apos;numericComplex&apos;, &apos;atLeastAlphabetic&apos;, &apos;atLeastAlphanumeric&apos;, &apos;alphanumericWithSymbols&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.androidWorkProfileRequiredPasswordType")]
        [Selectable]
        [ValidateSet(@"deviceDefault", @"lowSecurityBiometric", @"required", @"atLeastNumeric", @"numericComplex", @"atLeastAlphabetic", @"atLeastAlphanumeric", @"alphanumericWithSymbols")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;workProfilePasswordRequiredType&quot; property, of type &quot;microsoft.graph.androidWorkProfileRequiredPasswordType&quot;.")]
        public System.String workProfilePasswordRequiredType { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;workProfileRequirePassword&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidWorkProfileGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Password is required or not for work profile</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;workProfileRequirePassword&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean workProfileRequirePassword { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;securityRequireVerifyApps&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidWorkProfileGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Require the Android Verify apps feature is turned on.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileGeneralDeviceConfiguration", HelpMessage = @"The &quot;securityRequireVerifyApps&quot; property, of type &quot;Edm.Boolean&quot;.")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;securityRequireVerifyApps&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean securityRequireVerifyApps { get; set; }

        /// <summary>
        ///     <para type="description">A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.androidWorkProfileCustomConfiguration&quot; type.</para>
        /// </summary>
        [Selectable]
        [Expandable]
        [ParameterSetSelector(@"microsoft.graph.androidWorkProfileCustomConfiguration")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidWorkProfileCustomConfiguration", Mandatory = true, HelpMessage = @"A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.androidWorkProfileCustomConfiguration&quot; type.")]
        public System.Management.Automation.SwitchParameter androidWorkProfileCustomConfiguration { get; set; }

        /// <summary>
        ///     <para type="description">A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.androidGeneralDeviceConfiguration&quot; type.</para>
        /// </summary>
        [Selectable]
        [Expandable]
        [ParameterSetSelector(@"microsoft.graph.androidGeneralDeviceConfiguration")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", Mandatory = true, HelpMessage = @"A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.androidGeneralDeviceConfiguration&quot; type.")]
        public System.Management.Automation.SwitchParameter androidGeneralDeviceConfiguration { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;appsBlockClipboardSharing&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block clipboard sharing to copy and paste between applications.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;appsBlockClipboardSharing&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean appsBlockClipboardSharing { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;appsBlockYouTube&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the YouTube app.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;appsBlockYouTube&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean appsBlockYouTube { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;cellularBlockMessaging&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block SMS/MMS messaging.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;cellularBlockMessaging&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean cellularBlockMessaging { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;googleAccountBlockAutoSync&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block Google account auto sync.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;googleAccountBlockAutoSync&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean googleAccountBlockAutoSync { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;googlePlayStoreBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the Google Play store.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;googlePlayStoreBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean googlePlayStoreBlocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;kioskModeBlockSleepButton&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the screen sleep button while in Kiosk Mode.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;kioskModeBlockSleepButton&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean kioskModeBlockSleepButton { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;kioskModeBlockVolumeButtons&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the volume buttons while in Kiosk Mode.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;kioskModeBlockVolumeButtons&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean kioskModeBlockVolumeButtons { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;kioskModeApps&quot; property, of type &quot;microsoft.graph.appListItem&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">A list of apps that will be allowed to run when the device is in Kiosk Mode. This collection can contain a maximum of 500 elements.</para>
        /// </summary>
        [ODataType("microsoft.graph.appListItem")]
        [Selectable]
        [AllowEmptyCollection]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;kioskModeApps&quot; property, of type &quot;microsoft.graph.appListItem&quot;.")]
        public System.Object[] kioskModeApps { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;powerOffBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block powering off the device.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;powerOffBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean powerOffBlocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;factoryResetBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block user performing a factory reset.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;factoryResetBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean factoryResetBlocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;deviceSharingAllowed&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to allow device sharing mode.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;deviceSharingAllowed&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean deviceSharingAllowed { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;storageBlockGoogleBackup&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block Google Backup.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;storageBlockGoogleBackup&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean storageBlockGoogleBackup { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;storageRequireRemovableStorageEncryption&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to require removable storage encryption.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;storageRequireRemovableStorageEncryption&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean storageRequireRemovableStorageEncryption { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;voiceAssistantBlocked&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the use of the Voice Assistant.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;voiceAssistantBlocked&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean voiceAssistantBlocked { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;webBrowserBlockPopups&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block popups within the web browser.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;webBrowserBlockPopups&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean webBrowserBlockPopups { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;webBrowserBlockAutofill&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block the web browser&apos;s auto fill feature.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;webBrowserBlockAutofill&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean webBrowserBlockAutofill { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;webBrowserBlockJavaScript&quot; property, of type &quot;Edm.Boolean&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Indicates whether or not to block JavaScript within the web browser.</para>
        /// </summary>
        [ODataType("Edm.Boolean")]
        [Selectable]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;webBrowserBlockJavaScript&quot; property, of type &quot;Edm.Boolean&quot;.")]
        public System.Boolean webBrowserBlockJavaScript { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;webBrowserCookieSettings&quot; property, of type &quot;microsoft.graph.webBrowserCookieSettings&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">Cookie settings within the web browser.</para>
        ///     <para type="description">
        ///          Valid values: &apos;browserDefault&apos;, &apos;blockAlways&apos;, &apos;allowCurrentWebSite&apos;, &apos;allowFromWebsitesVisited&apos;, &apos;allowAlways&apos;
        ///     </para>
        /// </summary>
        [ODataType("microsoft.graph.webBrowserCookieSettings")]
        [Selectable]
        [ValidateSet(@"browserDefault", @"blockAlways", @"allowCurrentWebSite", @"allowFromWebsitesVisited", @"allowAlways")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;webBrowserCookieSettings&quot; property, of type &quot;microsoft.graph.webBrowserCookieSettings&quot;.")]
        public System.String webBrowserCookieSettings { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;appsInstallAllowList&quot; property, of type &quot;microsoft.graph.appListItem&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">List of apps which can be installed on the KNOX device. This collection can contain a maximum of 500 elements.</para>
        /// </summary>
        [ODataType("microsoft.graph.appListItem")]
        [Selectable]
        [AllowEmptyCollection]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;appsInstallAllowList&quot; property, of type &quot;microsoft.graph.appListItem&quot;.")]
        public System.Object[] appsInstallAllowList { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;appsLaunchBlockList&quot; property, of type &quot;microsoft.graph.appListItem&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">List of apps which are blocked from being launched on the KNOX device. This collection can contain a maximum of 500 elements.</para>
        /// </summary>
        [ODataType("microsoft.graph.appListItem")]
        [Selectable]
        [AllowEmptyCollection]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;appsLaunchBlockList&quot; property, of type &quot;microsoft.graph.appListItem&quot;.")]
        public System.Object[] appsLaunchBlockList { get; set; }

        /// <summary>
        ///     <para type="description">The &quot;appsHideList&quot; property, of type &quot;microsoft.graph.appListItem&quot;.</para>
        ///     <para type="description">This property is on the &quot;microsoft.graph.androidGeneralDeviceConfiguration&quot; type.</para>
        ///     <para type="description">List of apps to be hidden on the KNOX device. This collection can contain a maximum of 500 elements.</para>
        /// </summary>
        [ODataType("microsoft.graph.appListItem")]
        [Selectable]
        [AllowEmptyCollection]
        [Parameter(ParameterSetName = @"microsoft.graph.androidGeneralDeviceConfiguration", HelpMessage = @"The &quot;appsHideList&quot; property, of type &quot;microsoft.graph.appListItem&quot;.")]
        public System.Object[] appsHideList { get; set; }

        /// <summary>
        ///     <para type="description">A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.androidCustomConfiguration&quot; type.</para>
        /// </summary>
        [Selectable]
        [Expandable]
        [ParameterSetSelector(@"microsoft.graph.androidCustomConfiguration")]
        [Parameter(ParameterSetName = @"microsoft.graph.androidCustomConfiguration", Mandatory = true, HelpMessage = @"A switch parameter for selecting the parameter set which corresponds to the &quot;microsoft.graph.androidCustomConfiguration&quot; type.")]
        public System.Management.Automation.SwitchParameter androidCustomConfiguration { get; set; }
    }
}