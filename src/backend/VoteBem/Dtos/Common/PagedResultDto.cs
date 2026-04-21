namespace VoteBem.Dtos.Common
{
    public record PagedResultDto<T>
    {
        public IEnumerable<T> Data { get; set; } = null!;
        public int Page { get; set; }
        public int PageSize { get; set; }
        public int TotalItems { get; set; }
        public int TotalPages { get; set; }
        public bool HasPreviousPage { get; set; }
        public bool HasNextPage { get; set; }
    }

}
