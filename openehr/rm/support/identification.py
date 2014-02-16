# -*- coding: utf-8 -*-

"""
    Identification Package, support_im.pdf, Chapter 4
"""


import re
import inspect

from openehr.rm import RMObject


SEPARATOR = u"::"

class InvalidUID(ValueError):
    pass


class UID(object):
    """
        Abstract parent of classes representing unique identifiers
        which identify information entities in a durable way. UIDs only
        ever identify one IE in time or space and are never re-used.
 
        Instances of this class are immutable.
    """
    value = None

    def __init__(self, value):
        self.value = str(value)

    def __eq__(self, other):
        if not isinstance(other, UID):
            return False
        return self.value == other.value

    def __str__(self):
        return self.value

    def __hash__(self):
        return hash(self.value)


class ISO_OID(UID):
    u""" Model of ISO's Object Identifier (oid) as defined by the
    standard ISO/IEC 8824 .  Oids are formed from integers separated
    by dots. Each non-leaf node in an Oid starting from the left
    corresponds to an assigning authority, and identifies that
    authority's namespace, inside which the remaining part of the
    identifier is locally unique.
    """

    def __init__(self, value):
        super(ISO_OID, self).__init__(value)
        numbers_parts = self.value.split(".")
        for part in numbers_parts:
            if not part.isdigit(): raise InvalidUID("Invalid OID format. [%s]" % value)


class UUID(UID):
    u""" Model of the DCE Universal Unique Identifier or UUID which
    takes the form of hexadecimal integers separated by hyphens,
    following the pattern 8-4-4-4-12 as defined by the Open Group, CDE
    1.1 Remote Procedure Call specification, Appendix A. Also known as
    a GUID.

    Note: the java-lib implementation uses a less strict regular expression.
    so I followed that implementation instead of the spec.
    """

    __UUID_RE_STRICT = re.compile((r'\A([0-9a-fA-F]){8}'
                          r'-([0-9a-fA-F]){4}'
                          r'-([0-9a-fA-F]){4}'
                          r'-([0-9a-fA-F]){4}'
                          r'-([0-9a-fA-F]){12}\Z'))

    __UUID_RE = re.compile("([0-9a-fA-F])+(-([0-9a-fA-F])+)*")

    def __init__(self, value):
        if not self.__UUID_RE.match(value):
            raise InvalidUID("Invalid UUID format. [%s]" % value)
        super(UUID,self).__init__(value)


class InternetID(UID):
    u""" Model of a reverse internet domain, as used to uniquely
    identify an internet domain. In the form of a dot-separated string
    in the reverse order of a domain name specified by IETF RFC1034
    (http://www.ietf.org/rfc/rfc1034.txt).
    """

    __IETF_RE= re.compile((r'\A[a-zA-Z]'
                           r'([a-zA-Z0-9-]*'
                           r'[a-zA-Z0-9])?'
                           r'(\.[a-zA-Z]([a-zA-Z0-9-]*[a-zA-Z0-9]))+\Z'))


    def __init__(self, value):
        if not self.__IETF_RE.match(value):
            raise InvalidUID("Invalid Internet Domain. [%s]" % value)
        super(InternetID,self).__init__(value)


class ObjectID(RMObject):
    u"""
        Ancestor (abstract) class of identifiers of informational
        objects.  Ids may be completely meaningless, in which case their
        only job is to refer to something, or may carry some information
        to do with the identified object.  Object ids are used inside an
        object to identify that object. To identify another object in
        another service, use an OBJECT_REF, or else use a UID for local
        objects identified by UID. If none of the subtypes is suitable,
        direct instances of this class may be used.
    """
    value = None

    def __init__(self, value):
        self.value = str(value)

    def __eq__(self, obj):
        if obj is self:
            return True
        if isinstance(obj, ObjectID):
            return obj.value == self.value
        return False

    def __hash__(self):
        return hash(self.value)

    def __str__(self):
        return self.value

class UIDMatcher(object):
    def __init__(self, value):
        uid_factories = self.getUIDFactories()
        self.uid_obj = None
        for factory in uid_factories:
            try:
                self.uid_obj = factory(value)
            except InvalidUID:
                continue
            if self.uid_obj: break
        if self.uid_obj is None:
            raise InvalidUID("There isn't a UID that match. [%s]" % value)

    def getUIDFactories(self):
        return ( UUID, ISO_OID, InternetID ,)

    def createMatchedUid(self):
        return self.uid_obj


class UIDBasedID(ObjectID):
    """
        Abstract model of UID-based identifiers consisting of a root part and 
        an optional extension; lexical form: root "::" extension
    """
    _uid = None

    def __init__(self, uid, extension=None):
        value = u""
        if isinstance(uid, UID):
            self._uid = uid
            value = SEPARATOR.join(( uid.value , extension,))
        else:
            matcher = None
            if extension is not None:
                value = SEPARATOR.join(( uid , extension, ))
                matcher = UIDMatcher(uid)
            else:
                value = uid
                parts = self._split_parts(uid)
                matcher = UIDMatcher(parts[0])
            self._uid = matcher.createMatchedUid()
        super(UIDBasedID, self).__init__(value)

    def _split_parts(self, value):
        seploc = value.find(SEPARATOR)
        if seploc == 0:
            raise InvalidUID("The string doesn't have a valid UID. [%s]" % value)
        elif seploc == -1:
            return [value]
        elif len(value) == (seploc+2):
            raise InvalidUID("The string doesn't have a valid UID. [%s]" % value)
        else:
            root = value[:seploc]
            seploc+= 2
            extension = value[seploc:]
            parts = ( root, extension, )
            return parts

    @property
    def root(self):
        return self._uid

    @property
    def extension(self):
        parts = self._split_parts(self.value)
        if len(parts) == 2:
            return str(parts[1])
        else:
            return None

    def has_extension(self):
        if self.extension:
            return True
        return False


class HierObjectID(UIDBasedID):
    u""" 
        Hierarchical object identifiers.
 
        The syntax of the value attribute is as follows:
            root::extension
        with the extension bit optional

        Instances of this class are immutable.
    """


class ObjectVersionID(UIDBasedID):
    """
        Globally unique identifier for one version of a versioned object.

        The syntax of the value attribute is as follows:
        objectID::creatingSystemID::versionTreeID

        Instances of this class are immutable.
    """
    __object_id = None
    __creating_system_id = None
    __version_tree_id = None
    root_part = None
    extension_part = None

    def __init__(self, value, creatingSystemId=None, versionTreeId=None):

        if (type(value) == str and type(creatingSystemId) == str and
                type(versionTreeId) == str):
            value = SEPARATOR.join([value, creatingSystemId, versionTreeId])

        super(ObjectVersionID, self).__init__(value)

        splits = value.split(SEPARATOR)
        segments = len(splits)
        if segments == 0:
            raise ValueError('bad format, missing ObjectID')
        if segments < 3:
            raise ValueError('bad format, missing creatingSystemId or versionTreeId')
        if segments > 4:
            raise ValueError('bad format, too many segments or "::"')

        root_str = splits[0]
        uidmatcher = UIDMatcher(root_str)
        self.__object_id = uidmatcher.createMatchedUid()

        if segments == 4:
            self.__creating_system_id = HierObjectID(SEPARATOR.join(splits[1:3]))
            self.__version_tree_id = VersionTreeID(splits[3])
        else:
            self.__creating_system_id = HierObjectID(splits[1])
            self.__version_tree_id = VersionTreeID(splits[2])

        self.root_part = self.object_id
        self.extension_part = SEPARATOR.join((self.__creating_system_id.value, self.__version_tree_id.value,))

    def object_id(self):
        return self.__object_id

    def version_tree_id(self):
        return self.__version_tree_id

    def creating_system_id(self):
        return self.__creating_system_id

    def is_branch(self):
        return self.__version_tree_id.is_branch()



class TemplateID(ObjectID):
    """
        Identifier for templates. Lexical form to be determined.
    """
    pass


class TerminologyID(ObjectID):
    """
        Terminology identifier. Instances of this class are immutable.
    """
    __name = __version = None

    def __init__(self, name, version=None):
        if version == None:
            parts = name.partition('(')
            self.__name = parts[0]
            self.__version = parts[2].rstrip(')') or None
        else:
            self.__name, self.__version = name, version
            name = '%s(%s)' % (name, version)
        self.value = name
        super(TerminologyID,self).__init__(name)

    def name(self):
        return self.__name

    def version_id(self):
        return self.__version

    def __repr__(self):
        return 'TerminologyID(%s)' % self.value

class VersionTreeID(object):
    """
        Version tree identifier for one version
        The format of the identifier is:
        <trunk_version>[.<branch_number>.<branch_version>]
    """

    __PATTERN = re.compile(r"[1-9](\d)*(\.(\d)+\.(\d)+)?")

    __branch_number = None
    __branch_version = None
    __trunk_version = None

    def __init__(self, value, branchNo=None, branchV=None):
        """
            Take either 3 values or one value in format x.y.z.
        """
        if branchNo == None:
            match = self.__PATTERN.match(value)
            if (match is None) or (match.start() != 0) or (match.end() != len(value)):
                raise ValueError('wrong format')

            branch = value.find('.')
            if branch < 0: # no branch, just trunk
                self.__trunk_version = value
                self.value = value
            else:
                entries = value.split(".")
                self.__validate_values(int(entries[0]),
                                       int(entries[1]),
                                       int(entries[2]))
                self.__trunk_version = entries[0]
                # never set branchNo or branchV to 0
                if int(entries[1]) > 0:
                    self.__branch_number = entries[1]
                    self.__branch_version = entries[2]
                    self.value = value
                else:
                    self.value = entries[0]
        else:
            value = int(value)
            branchNo = int(branchNo)
            branchV = int(branchV)
            self.__validate_values(value, branchNo, branchV)
            self.value = self.__trunk_version = str(value)
            if int(branchNo) > 0:
                # never set branchNo or branchV to 0
                self.__branch_number = str(branchNo)
                self.__branch_version = str(branchV)
                self.value = self.value + '.' + str(branchNo) + '.' + str(branchV)

    def __validate_values(self, trunk, branchNo, branchV):
        if (trunk < 1) or (branchNo < 0) or (branchV < 0):
            raise ValueError('version number smaller than 0')

        # 0 for branchNo or branchV is special case,
        # where both must be 0 to indicate no branch
        if (branchNo == 0) or (branchV == 0):
            if branchV != branchNo:
                raise ValueError('breach of branch_validity')

    def trunk_version(self):
        return self.__trunk_version

    def branch_number(self):
        return self.__branch_number

    def branch_version(self):
        return self.__branch_version

    def is_branch(self):
        return not self.__branch_version is None

    def is_first(self):
        return self.__trunk_version == '1' and (not self.is_branch())

    def next(self):
        """
            This appears not to be part of the spec, but it is implemented
            in the java version and is needed to pass the unit tests.
        """
        if self.is_branch():
            return VersionTreeID(self.trunk_version(),
                    self.branch_number(),
                    str(int(self.branch_version()) + 1))
        else:
            return VersionTreeID(str(int(self.trunk_version()) + 1))

    def __eq__(self, other):
        if not isinstance(other, VersionTreeID):
            return False
        return self.value == other.value

    def __str__(self):
        return str(self.value)


class ArchetypeID(ObjectID):
    """
        Identifier for archetypes, instances of this class are immutable.
    """

    __AXIS_SEPARATOR = u'.'
    __SECTION_SEPARATOR = u'-'
    # Note - I weakened this validation from the oship implementation
    __NAME_PATTERN = re.compile(r"[a-zA-Z][a-zA-Z0-9()_/%$#&\.-]*")
    __VERSION_PATTERN = re.compile(r"[a-zA-Z0-9]+")

    __qualified_rm_entity = __domain_concept = __version = None
    __rm_originator = __rm_name = __rm_entity = None
    __conceptName = __specialisation = None

    def _toDomainConcept(self, conceptName, specialisation):
        return (conceptName or '') + self.__SECTION_SEPARATOR + self.__SECTION_SEPARATOR.join(specialisation)

    def _toValue(self, rmOriginator, rmName, rmEntity, conceptName, specialisation, versionID):
        return ''.join([
                self.__SECTION_SEPARATOR.join([rmOriginator or '', rmName or '', rmEntity or '']),
                self.__AXIS_SEPARATOR, self._toDomainConcept(conceptName, specialisation),
                self.__AXIS_SEPARATOR, versionID or ''])
    

    def __init__(self, value,
        rmName=None, rmEntity=None, conceptName=None, specialisation=None, versionID=None):
        if rmName != None:
            rmOriginator = value
            if type(specialisation) != list:
                if specialisation == None:
                    specialisation = []
                else:
                    specialisation = [specialisation]
            value = self._toValue(rmOriginator, rmName, rmEntity, conceptName, specialisation, versionID)
            super(ArchetypeID,self).__init__(value)

            self.__rm_originator = rmOriginator
            self.__rm_name = rmName
            self.__rm_entity = rmEntity
            self.__conceptName = conceptName
            self.__specialisation = specialisation
            self.__version = versionID

            self.__domain_concept = self._toDomainConcept(conceptName, specialisation)
            self.__qualified_rm_entity = self.__SECTION_SEPARATOR.join([rmOriginator or '', rmName or '', rmEntity or ''])

            if self.__version != None:
                self.__validate_version_id(self.__version)
            self.__validate_name(self.__rm_originator, 'rm_originator')
            self.__validate_name(self.__rm_name,'rm_name')
            if self.__rm_entity != None:
                self.__validate_name(self.__rm_entity, 'rm_entity')
            if self.__conceptName != None:
                self.__validate_name(self.__conceptName, 'concept_name')

        else:
            super(ArchetypeID,self).__init__(value)

            tokens = value.split(self.__AXIS_SEPARATOR)
            if len(tokens) != 3:
                raise ValueError('bad format, wrong number of sections')
            self.__qualified_rm_entity = tokens[0]

            self.__domain_concept = tokens[1]
            self.__version = tokens[2]
            self.__validate_version_id(self.__version)

            tokens = self.__qualified_rm_entity.split(self.__SECTION_SEPARATOR)
            if len(tokens) != 3:
                raise ValueError('bad format, wrong number of sections in ' + self.value)
            self.__rm_originator = tokens[0]
            self.__validate_name(self.__rm_originator, 'rm_originator')
            self.__rm_name = tokens[1]
            self.__validate_name(self.__rm_name,'rm_name')
            self.__rm_entity = tokens[2]
            self.__validate_name(self.__rm_entity, 'rm_entity')

            tokens = self.__domain_concept.split(self.__SECTION_SEPARATOR)
            if len(tokens) < 1:
                raise ValueError('bad format, too few sections for domainConcept in ' + self.value)
            self.__conceptName = tokens[0]
            self.__validate_name(self.__conceptName, 'concept_name')
            if len(tokens) > 1:
                for t in tokens[1:]:
                    self.__validate_name(t, 'specialisation')
                self.__specialisation = tokens[1:]
            else: self.__specialisation = None

    def __validate_name(self, value, label):
        match = self.__NAME_PATTERN.match(value)
        if (match is None) or (match.end() < len(value)):
            raise ValueError('wrong format of ' + label + ': ' + value)

    def __validate_version_id(self, version):
        match = self.__VERSION_PATTERN.match(version)
        if (match is None) or (match.end() < len(version)):
            raise ValueError('wrong format of versionId: ' + version)

    @property
    def qualified_rm_entity(self):
        return self.__qualified_rm_entity

    @property
    def concept_name(self):
        return self.__concept_name

    def domain_concept(self):
        return self.__domain_concept

    def rm_originator(self):
        return self.__rm_originator

    def rm_name(self):
        return self.__rm_name

    def rm_entity(self):
        return self.__rm_entity

    def specialisation(self):
        return self.__specialisation

    def version_id(self):
        return self.__version

    @property
    def base(self):
        """
            A base of the archetypeId is the value of it without versionId
        """
        return ''.join([
            self.__SECTION_SEPARATOR.join(
                [self.rm_originator() or '', self.rm_name() or '', self.rm_entity() or '']),
            self.__AXIS_SEPARATOR, self.domain_concept() or ''])

    def __eq__(self, other):
        if not isinstance(other, ArchetypeID):
            return False
        return self.base == other.base

class GenericID(ObjectID):
    """
        Generic identifier type for identifiers whose format is otherwise unknown 
        to openEHR. Includes an attribute for naming the identification scheme 
        (which may well be local).
    """
    scheme = None
    def __init__(self, value, scheme):
        self.scheme=scheme
        super(GenericID,self).__init__(value)

    def __eq__(self, other):
        if not isinstance(other, GenericID):
            return False
        if self.value != other.value:
            return False
        return self.scheme == other.scheme

    def __hash__(self):
        return super(GenericID, self).__hash__() + hash(self.scheme)

class ObjectRef(RMObject):
    """
        Class describing a reference to another object, which may exist
        locally or be maintained outside the current namespace, eg in
        another service. Services are usually external, eg available in
        a LAN (including on the same host) or the internet via Corba, SOAP,
        or some other distributed protocol. However, in small systems they
        may be part of the same executable as the data containing the Id. 
    """

    type_ = id_ = namespace_ = None

    def __init__(self, obj_or_uid, namespace, type_=None):
        if isinstance(obj_or_uid, ObjectID):
            id_ = obj_or_uid
            if type_ is None:
                raise AttributeError(("A type must be a passed when a id object is"
                                      " provided instead of a object."))
        else:
            id_ = obj_or_uid.id
            if type_ is None:
                type_ = str(obj_or_uid.__class__.__name__)
        self.id_ = id_
        if namespace == None:
            raise AttributeError("A namespace is required")
        self.namespace_ = str(namespace)
        self.type_= str(type_)

    def __eq__(self, other):
        """
        Equality method necessary to include the
        object itself in a set collection.
        """
        if isinstance(other, ObjectRef):
            return hash(self) == hash(other)

    def __ne__(self,other):
        return not self.__eq__(other)

    def __hash__(self):
        """
        Hash method necessary to include the
        object itself in a set collection. 
        """
        rv = hash(self.id.value)
        if self.namespace_:
            rv = rv+ hash(self.namespace_)
        if self.type_:
            rv = rv+ hash(self.type_)
        return rv

    @property
    def id(self):
        return self.id_

    @property
    def namespace(self):
        return self.namespace_

    @property
    def type(self):
        return self.type_

class AccessGroupRef(ObjectRef):
    u""" Reference to access group in an access control service. """

    def __init__(self, obj_or_uid, namespace=None, type_=None):
        if namespace == None:
            super(AccessGroupRef, self).__init__(obj_or_uid, "ACCESS_CONTROL", "ACCESS_GROUP")
        else:
            super(AccessGroupRef, self).__init__(obj_or_uid, namespace, type_)

class LocatableRef(ObjectRef):

    def __init__(self,version_object, path_or_obj=None, namespace=u"",type_=None):
        path = ""
        obj = None
        if path_or_obj is None:
            path = ""
            obj = version_object.data
        elif isinstance(path_or_obj,str):
            path = path_or_obj
            data = version_object.data
            if not data.pathExists(path):
                raise AttributeError(("The path %s is not found on the" 
                                      " Versioned structure.") %path)
            obj=data.itemAtPath(path)
        else:
            obj = path_or_obj
            if obj.isArchetypeRoot(): path = ""
            else: path = version_object.data.pathOfItem(obj)

        if type_ is None:
            type_ = str(obj.__class__.__name__)
        version_id = version_object.uid
        super(LocatableRef,self).__init__(version_id,namespace,type_)

        if len(path): path = str(path)
        else: path = None
        self.path = path

    def as_uri(self):
        if self.path is None:
            path_str = ""
        else: path_str = self.path
        return str('/'.join(['ehr:/', self.id.value,path_str]))

    def __eq__(self, other):
        if isinstance(LocatableRef, other):
            return hash(self) == hash(other)

    def __hash__(self):
        return hash(self.as_uri())


class PartyRef(ObjectRef):
    """
        Identifier for parties in a demographic service. There are
        typically a number of subtypes of the "PARTY" class, including
        "PERSON", "ORGANISATION", etc.
    """

    def __init__(self,objectid_or_party_obj,namespace,type_=None):
        id_ = None
        if isinstance(objectid_or_party_obj, ObjectID):
            objectid = objectid_or_party_obj
            id_ = objectid
        else:
            party_object = objectid_or_party_obj
            super_class_names = [ klass.__name__ for klass in inspect.getmro(party_object.__class__) ]
            is_party_instance = 'Party' in super_class_names
            is_actor_instance = 'Actor' in super_class_names
            type_ = party_object.__class__.__name__
            is_a_valid_type = self.partyref_type_is_valid(type_)
            if is_actor_instance and is_party_instance and not is_a_valid_type :
                type_ = u'ACTOR'
            elif is_party_instance and not is_a_valid_type:
                type_ = u'PARTY'
            elif is_party_instance and is_a_valid_type:
                type_ = type_.upper()
            else: raise ValueError("The object must be a Party object.")
            id_ = party_object.uid
        super(PartyRef,self).__init__(id_,namespace,type_,)

    def partyref_type_is_valid(self, type_):
        return True if type_.upper() in [u'PERSON',
                                  u'ORGANISATION',
                                  u'GROUP',
                                  u'AGENT',
                                  u'ROLE',
                                  u'PARTY',
                                  u'ACTOR'] else False


