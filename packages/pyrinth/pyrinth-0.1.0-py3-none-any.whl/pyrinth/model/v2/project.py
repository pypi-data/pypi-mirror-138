from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Any

from pyrinth._util import Deprecated, datetimeFromString
from pyrinth.internal.cacheManager import CachedObject
from pyrinth.internal.lazy import LazyObject
from pyrinth.model.license import License
import pyrinth.model.v2 as v2
from pyrinth.model.v2.enums import Category, SupportStatus, ProjectStatus, ProjectType
from pyrinth.model.v2.projectVersion import ProjectVersion


__all__ = [
	'Project',
	'LazyProject'
]


@dataclass
class Project:
	slug: Optional[ str ]  #: The slug of a project, used for vanity URLs
	title: str  #: The title or name of the project
	description: str  #: A short description of the project
	categories: list[Category]  #: A list of the categories that the project is in
	client_side: SupportStatus  #: The client side support of the project
	server_side: SupportStatus  #: The server side support of the project
	body: str  #: A long form description of the mod
	status: ProjectStatus  #: The status of the project
	license: License  #: The license of the project
	issues_url: Optional[str]  #: An optional link to where to submit bugs or issues with the project
	source_url: Optional[str]  #: An optional link to the source code of the project
	wiki_url: Optional[str]  #: An optional link to the project's wiki page or other relevant information
	discord_url: Optional[str]  #: An optional invite link to the project's discord
	donation_urls: list[ str ]  #: A list of donation links for the project
	project_type: ProjectType  #: The project type of the project
	downloads: int  #: The total number of downloads of the project
	followers: int  #: The total number of users following the project
	icon_url: Optional[str]  #: The URL of the project's icon
	id: str  #: The ID of the project, encoded as a base62 string
	team: str  #: The ID of the team that has ownership of this project
	moderator_message: Optional[str]  #: A message that a moderator sent regarding the project
	published: datetime  #: The date the project was published
	updated: datetime  #: The date the project was last updated
	versions: list[ ProjectVersion ]  #: A list of the versions of the project
	gallery: list  #: A list of images that have been uploaded to the project's gallery
	body_url: Deprecated[str] = Deprecated( reason='Now the body is included in the object directly' )  #: The link to the long description of the project

	@classmethod
	def fromJson( cls, kwargs: dict[ str, Any ] ) -> 'Project':
		kwargs['client_side'] = SupportStatus[ kwargs['client_side'].upper() ]
		kwargs['server_side'] = SupportStatus[ kwargs['server_side'].upper() ]
		kwargs['status'] = ProjectStatus[ kwargs['status'].upper() ]
		kwargs['license'] = License.of( **kwargs['license'] )
		kwargs['project_type'] = ProjectType[ kwargs['project_type'].upper() ]
		kwargs['published'] = datetimeFromString( kwargs['published'] )
		kwargs['updated'] = datetimeFromString( kwargs['updated'] )
		kwargs[ 'categories' ] = Category.forList( kwargs[ 'categories' ] )
		kwargs[ 'versions' ] = ProjectVersion.forList( kwargs[ 'versions' ] )
		return Project( **kwargs )


class LazyProject( CachedObject[Project], LazyObject[Project] ):
	_projectid: str

	def __init__( self, projectid: str ):
		self._projectid = projectid

	def _populate( self ) -> None:
		value = LazyProject.getObject( self._projectid )
		if value is None:
			value = Project.fromJson( v2.getRequest( f'project/{self._projectid}' ).json() )
			LazyProject.setObject( self._projectid, self._impl )
		self._impl = value
