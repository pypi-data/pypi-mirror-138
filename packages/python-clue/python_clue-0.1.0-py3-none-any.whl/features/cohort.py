from typing import List
from clue_pb2 import (
    RequestCohortList,
    RequestCohortStream
)

from pyclue.converter import convert
from pyclue.stream import Stream


class CohortFeatures:
  @convert()
  def get_cohort_list(
      self,
      page: int = 1,
      length: int = 0,
      term: str = ""
  ) -> List[dict]:
    """
    Get the list of cohorts.

    :param int page:
      Page number.
    :param int length:
      Number of cohorts in a page. If 0, all cohorts will be returned.
    :param str term:
      Search term.

    :return: List of cohorts.
    :rtype: List of dictionaries.
    """
    cohort_list = self.stub.GetCohortList(RequestCohortList(
        term=term,
        page=page,
        length=length,
    )).cohort_list

    return cohort_list

  def get_cohort_person_table(self, cohort_id: int) -> Stream:
    """
    Get person table of a cohort.
    Data stream connection will be opened.

    :param int cohort_id:
      ID of the cohort.

    :return: Stream object.
    :rtype: Stream
    """
    return Stream(
        self.stub.GetCohortPersonTable,
        RequestCohortStream,
        cohort_id=cohort_id
    )
