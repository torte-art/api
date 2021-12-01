export enum State {
  PENDING = 'PENDING',
  COMPLETED = 'COMPLETED',
  FAILED = 'FAILED',
}

export enum KycDocument {
  CHATBOT = 'chatbot-onboarding',
  ADDITIONAL_INFORMATION = 'additional-information',
  ADDRESS_CHECK = 'address-check',
  API_CHECK = 'api-check',
  API_UPLOAD_FINANCIAL_STATEMENT = 'api-upload-financial-statement',
  API_UPLOAD_IDENTIFICATION_DOCUMENT = 'api-upload-identification-document',
  APPROVAL_DOCUMENT = 'approval-document',
  BCP = 'bcp',
  BENEFICIAL_OWNER = 'beneficial-owner',
  CERTIFICATE_INHERITANCE = 'certificate-inheritance',
  CHATBOT_ONBOARDING = 'chatbot-onboarding',
  CHATBOT_VERIFICATION = 'chatbot-verification',
  CHECK = 'check',
  COMPLIANCE_CHECK = 'compliance-desk',
  CONTROLLER = 'controller',
  CRYPTO_CURRENCY_PROPERTIES = 'crypto-currency-properties',
  EDD = 'edd',
  FINANCIAL_STATEMENTS = 'financial-statements',
  INCORPORATION_CERTIFICATE = 'incorporation_certificate',
  INVOICE = 'invoice',
  MRZ = 'mrz',
  ONLINE_IDENTIFICATION = 'online-identification',
  PASSPORT_OR_ID = 'passport_or_id',
  REGISTRY_COMMERCE = 'registry_commerce',
  REPRESENTATION = 'representation',
  STATUTES_ASSOCIATION = 'statutes-association',
  TAX_DECLARATION = 'tax-declaration',
  USER_ADDED_DOCUMENT = 'user-added-document',
  VERIFICATION = 'verification',
  VIDEO_IDENTIFICATION = 'video_identification',
}

export interface Challenge {
  key: string;
  challenge: string;
}

export interface CheckResponse {
  customerReference: string;
  customerId: number;
  customerVersionId: number;
  checkId: number;
  checkTime: number;
  riskState: string;
}

export interface CreateResponse {
  customerReference: string;
  customerId: number;
  customerVersionId: number;
}

export interface ChatBotResponse {
  document: string;
  reference: string;
  sessionUrl: string;
  version: string;
}

export interface IdentificationResponse {
  document: string;
  reference: string;
  version: string;
}

export interface CheckVersion {
  name: string;
  state: State;
  creationTime: number;
  modificationTime: number;
}

export interface CheckResult {
  checkId: number;
  checkTime: number;
  matchIds: number[];
  risks: Risk[];
}

export interface Risk {
  criterionKey: string;
  categoryKey: string;
}

export interface Customer {
  reference: number;
  type: string;
  id?: number;
  versionId?: number;
  names: [{ firstName: string; lastName: string }];
  datesOfBirth: [{ year: string; month: string; day: string }];
  citizenships: [string];
  countriesOfResidence: [string];
  emails: [string];
  telephones: [string];
  structuredAddresses: [
    {
      street: string;
      houseNumber: string;
      zipCode: string;
      city: string;
      countryCode: string;
    },
  ];
  gender: string;
  title: string;
  preferredLanguage: string;
  activationDate: { year: string; month: string; day: string };
  deactivationDate: { year: string; month: string; day: string };
}

export interface CustomerInformationResponse {
  reference: string;
  contractReference: string;
  contractState: string;
  lastCheckId: number;
  lastCheckTime: number;
  lastCheckVerificationId: number;
}